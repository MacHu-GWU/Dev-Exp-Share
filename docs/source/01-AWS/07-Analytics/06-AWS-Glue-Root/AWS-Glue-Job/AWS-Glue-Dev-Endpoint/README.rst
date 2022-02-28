AWS Glue Dev Endpoint
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


What is Glue Dev Endpoint
------------------------------------------------------------------------------
Glue Dev Endpoint 的目的是让开发者能有一个像平时开发用的 IDE / Code Editor 那样的环境, 能够 **交互式开发** 并测试输出. 很多开发者都是直接在 Glue Job 中写 ETL Script 然后点击 Run 运行, 这样获得反馈的时间需要起码 1 分钟, 因为 Run Glue Job 需要一些冷启动时间.

在 Hadoop Spark 生态中, 开发者常用 Zeppelin Notebook 或 Jupyter Notebook 连接 Spark 集群进行 **交互式开发**. 但由于 Glue 本质上是 Serverless 的 Spark, 开发者无法控制底层的集群, 集群可供按照 Notebook 应用. 而 Glue Dev Endpoint 本质上是临时创建的小型 Spark 集群, 而 Notebook 可以使用 AWS Sagemaker Notebook. AWS 做了一些工作将其打通, 几下点击后开发者就有了一个 Glue ETL **交互式开发** 的环境了. (启动 Dev Endpoint 需要大约 5-6 分钟, 启动 Notebook 也需要大约 5-6 分钟, 然后将 Notebook 将其绑定到 Dev Endpoint 也需要大约 3-5 分钟)

用户可以将在 Notebook 上的代码用 Git 保存. 而只在有需要的时候启动 Glue Dev Endpoint 即可.


How Dev Endpoint work with Sagemaker Notebook
------------------------------------------------------------------------------
Sagemaker Notebook 是大多人做 ETL development 的选择. 所以理解 Sagemaker Notebook 是如何和 Dev Endpoint 配合的很有必要.

我们知道 Dev Endpoint 本质上就是一个 Spark cluster. Jupyter Notebook 有一个插件叫做 SparkMagic, 可以将 Spark job 提交给远程的 Spark cluster. 而 Spark cluster 上有个软件叫做 Apache Livy, 可以对外提供 rest api 以调用 Spark 接口. 简单来说你在 Jupyter Notebook 上运行一行代码时, 实际发生了::

    Jupyter
    ->
    SparkMagic
    ->
    network
    ->
    AWS Glue development endpoint
    ->
    Apache Livy
    ->
    Apache Spark

一个 Jupyter Notebook App 上可以有很多个 Notebook 文件, 每个 Notebook 文件本质上是一个能和 Jupyter Notebook Kernel 通信的 session. 而每次 SparkMagic submit job 到 Spark 时, Livy 就会创建一个 Livy-session-N. **总结来说 Jupyter Notebook 文件 Notebook session, Livy Session 是一一对应的关系. 你可以打开多个 Notebook, 每个对应一个 Livy Session**. Livy session 在你 Shutdown Jupyter Notebook Kernel 后会自动断开, 而且长时间没有反应是会 timeout 的.

Ref:

- https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint-how-it-works.html

https://docs.aws.amazon.com/cli/latest/reference/glue/update-dev-endpoint.html

.. code-block:: bash

    aws glue update-dev-endpoint --endpoint-name sanhe-dev --custom-libraries ExtraPythonLibsS3Path=s3://aws-data-lab-sanhe-for-everything-us-east-2/glue/artifacts/python-library/etl-job.zip


Glue Dev Endpoint with Python
------------------------------------------------------------------------------


Ref:

- Glue Dev Endpoint 中 Glue 的版本信息: https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint.html
- Glue Dev Endpoint 中自带的 Python 库的信息: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue20-modules-provided
- 关于 Glue Dev Endpoint 无法添加依赖 C 的包的声明: https://docs.aws.amazon.com/glue/latest/dg/add-dev-endpoint.html
- Glue Release Note: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html


Links
------------------------------------------------------------------------------
- Using Python Libraries with AWS Glue (如何给 Glue Job 或者 Glue Dev Endpoint 添加 Python library dependency): https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#aws-glue-programming-python-libraries-zipping
- Using Development Endpoint (Dev endpoint 可以跟很多开发环境联通, 这里有个全面的列表): https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint.html