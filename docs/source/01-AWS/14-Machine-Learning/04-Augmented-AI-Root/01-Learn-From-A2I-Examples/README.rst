Learn From A2I Examples
==============================================================================
Keyword: A2I, HIL, Task Template, Example, Examples

搭建一个 Human In Loop 系统 50% 以上的难点就是创建一个合适的 Task Template. 所以为了提高 Task Template 的开发速度, 我创建了一个简单的脚本方便开发者 Debug.

如果你完全没有经验, 从 https://github.com/aws-samples/amazon-a2i-sample-task-uis 上面的例子开始学习可能是最快的. 这个文件夹里的一些脚本能够方便的让你从 ``amazon-a2i-sample-task-uis`` repo 上 Copy 代码并且在真正的 HIL 上预览到时候做 Labeling 工作的人看到的 UI 效果.

除此之外, 你还可以到这篇 Crowd HTML reference https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html 文档中学习如何有哪些 HTML 元素可以用. 里面还提供了一个 CodePen 的工具, 可以用于预览 HTML + JavaScript 的效果.


如何使用这个脚本
------------------------------------------------------------------------------
这里我们一共有 4 个重要文件:

- ``requirements.txt``: 该脚本所需的依赖. 你要先 ``pip install -r requirements.txt`` 才能运行 ``script.py`` 脚本
- ``task.liquid``: Task Template 的 HTML 模版. 你在 ``amazon-a2i-sample-task-uis`` repo 上 Copy 的代码, 或是你自己写的 HTML 模版放到到这个文件. 之后我们会用脚本将其部署到 AWS.
- ``task.json``: 你开启一个 HIL 的时候是需要给定一些 Data 的, 这样 html template 才能 render 出一个合适的 UI, 你在调用 ``start_human_loop`` 之前要确保这个 JSON 正确.
- ``script.py``: 是一个自动化的 Python 脚本, 你可以用它来快速的尝试 ``task.liquid`` 和 ``task.json`` 来预览最终的效果. 这个 ``script.py`` 主要就干三件事 (都是发生在 AWS 端, 不是发生在你的本地):
    1. 删除已经存在的 Task Template
    2. 创建新的 Task Template
    3. 用新创建的 Task Template + JSON 来运行一个 HIL, 看看效果.


.. literalinclude:: ./task.liquid
   :language: html

.. literalinclude:: ./task.json
   :language: json

.. literalinclude:: ./script.py
   :language: python
