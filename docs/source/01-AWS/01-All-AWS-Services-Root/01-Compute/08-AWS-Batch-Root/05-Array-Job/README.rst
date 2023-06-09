Array Job
==============================================================================
Keywords: AWS Batch, Array Job, Jobs.


1. What is Array Job?
------------------------------------------------------------------------------
Array Job 是你在 Submit Job 的时候的一种运行模式. 是一组 Parameter, Environment Variable 都相同的 Job 的集合. 唯一的不同点是他们的 Runtime 里有一个 Environment Variable ``AWS_BATCH_JOB_ARRAY_INDEX``, 其中值是 ``${example_job_ID}:${index}``, 例如 ``49970833-3524-4e37-9ab2-a5b2057d2bf9:0``, ``49970833-3524-4e37-9ab2-a5b2057d2bf9:1``, ...

注意, 这和你有一个能接受不同参数的程序, 然后用不同的参数同时运行这个程序不一样. 这里的 Array Job 在调度层面是无法给它不同的参数的. 这个机制是用来运行大规模高度并行计算的. 例如蒙特卡洛模拟 (同样的参数模拟 1000 次, 得到不同的结果), CG 图标渲染等.

Reference:

- `Array Jobs <https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html>`_


2. Array Job vs Multi-Invocations
------------------------------------------------------------------------------
前面我们讲了 Array Job 是无法输入不同的参数的, 如果将 Job 想象为一个函数, 那么 Array Job 的本质像是这样:

.. code-block:: python

    kwargs = {"key": "value"}
    for _ in range(100):
        batch_client.run_job(kwargs=kwargs)

而用不同的参数运行一个函数很多次 (multi-invocations) 的本质则是这样:

.. code-block:: python

    kwargs_list = [
        {"key": "value1"},
        {"key": "value2"},
        ...
        {"key": "value100"},
    ]
    for kwargs in kwargs_list:
        batch_client.submit_job(kwargs=kwargs)

你可以看出两者之间的调用逻辑的不同. 我认为之所以 AWS 是这么设计是应为后一种方式在业内的解决方案非常多, 没有必要重新造轮子. 而第一个方式是高度并行的, 这些工作的特点是并行度高, 并且开销极大, 商业利润也很高, 并且市场上针对该情况高度优化的产品很少, 所以 AWS 才做了这么一个产品.


3. Container App that support Single Job and Array Job
------------------------------------------------------------------------------
上一节我们了解了 Array Job 和 Multi Invocation 的区别, 它们的编程模型是不同的. 那么有没有一种方法我们只构建一次 App, 然后既可以支持 Array Job, 又可以支持 Multi Invocation 呢?

答案是当然可以. 我们来看下面这个例子. 它是用于将一个 S3 folder 中的文件拷贝到另一个 S3 folder 中. 里面有一个 ``copy_s3_folder`` 函数实现了核心逻辑并定义了参数. 而我们将其包装成了一个 CLI 应用.

.. literalinclude:: ./main_old.py
   :language: python
   :linenos:

我们可以在不改变核心逻辑的情况下对 CLI app 进行改造. 我们在已有的参数基础上, 增加了一个参数 s3uri_kwargs, 用于从 S3 中读取参数.

1. 如果 s3uri_kwargs 为 None, 则直接使用 s3uri_source 和 s3uri_target 作为参数.
    就像直接使用 :func:`copy_s3_folder` 一样.
2. 如果 s3uri_kwargs 不为 None, 则从 S3 中的 JSON 文件中读取参数, 并使用这些参数作为参数.

.. literalinclude:: ./main_new.py
   :language: python
   :linenos:

这样我们如果要运行 Array Job 的时候, 只要预先把并行的输入参数保存到 S3 上 (很多个小文件), 然后输入的命令是 ``python main.py copy-s3-folder --s3uri-kwargs s3://my-bucket/kwargs`` 即可. 如果我们要 Multi Invocation,  那么输入的命令是 ``python main.py copy-s3-folder --s3uri-source s3://my-bucket/source --s3uri-target s3://my-bucket/target``.


4. 如何编排 Multi Invocation
------------------------------------------------------------------------------
前面我们说了 Multi Invocation 的编排在业内已经有很多解决方案了, 那我们就来快速的过一遍这些方案.

**方法 1**, 手动调用 `submit_job API <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/client/submit_job.html>`_ 许多次:

.. code-block:: python

    kwargs_list = [
        {"key": "value1"},
        {"key": "value2"},
        ...
        {"key": "value100"},
    ]
    for kwargs in kwargs_list:
        batch_client.submit_job(kwargs=kwargs)

这样就相当于一个异步调用了. 这是最简单也是最直接的办法.

**方法 2**. 使用 `AWS StepFunctions <https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html>`_, 其中第一步用 Lambda 来准备好 ``kwargs_list`` 中的数据, 然后直接返回这个数据, 而不要直接用 API 调用. 然后用 `Map State <https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html>`_ 将其分发出去并行执行. 这样做的好处是每一个 Job 都是有追踪的, 而无需自己去实现, 可以知道哪些成功了哪些没有成功. 而且它有允许一定的失败百分比的功能.

**方法 3**. 使用 Array Job, 上一节中提到的方法运行 Job.


5. Failure in Array Job
------------------------------------------------------------------------------
一旦涉及到并行计算, 那么错误的处理是一个绕不开的话题. 因为对于错误的处理是完全基于你的业务的. 通常业内会有这么几种需求, 我也附上了对应的解决方案.

1. 一旦有一个 Job 失败, 那么整个 Array Job 就失败. 所有在运行中的 Job 都停止, 整个 Job 废弃. 该情况常用于所有的 Job 之间联动, 并且是不是幂等, 对运行的事件敏感的情况 (就是现在运行和之后运行的结果是不同的, 所以无法重试). 这种情况就用默认的 Array Job 即可.
2. 允许一定比例的 Job 失败, 对失败的 Job 不进行重试, 所有在运行中的 Job 继续运行. 例如在进行蒙特卡洛模拟的时候, 部分失败了也没有关系, 不影响整体模拟的准确性. 如果对失败的部分进行重试从逻辑上来说会导致模拟结果有变差, 所以我们不重试. 这种情况可以不能用 Array Job, 而是要用 AWS StepFunction + Map State + ToleratedFailurePercentage 功能来实现.
3. 允许部分 Job 失败, 所有在运行中的 Job 继续进行. 之后对失败的 Job 进行重试. 这适合于 Job 幂等的情况 (输入一样那么输出也一样, 现在运行和之后运行结果也一样). 这种情况可以不能用 Array Job, 而是要用, 而是直接用 Async Call 来运行, 然后用 DynamoDB 来 track 每个 Job 的成功失败状态.
