.. _aws-a2i-custom-task-template-example:

Custom Task Template Example
==============================================================================
Keywords: AWS Augmented AI, a2i, human in loop, HIL, Task Template

对 A2I 进行自定义的关键就是定义 Task Template, 因为 Task Template 定义了 HIL Task Input Data, Output Data 转换关系, 以及最关键的 UI.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 准备工作
------------------------------------------------------------------------------
首先你需要在 `GroundTruth AWS Console <https://console.aws.amazon.com/sagemaker/groundtruth?#/labeling-workforces>`_ 手动创建 Private Workforce Team, 并邀请至少 1 位员工加入这个 Team.



2. 开发 Task Template
------------------------------------------------------------------------------

准备 Task Input 的数据, 需要包含你的 Computational 的 Input / Output 以及计算所需的参考信息.

.. literalinclude:: ./task.json
   :language: json

开发 UI HTML 模板, 把这些信息用 Human Friendly 的形式排版好.

.. literalinclude:: ./task.html
   :language: html

运行这个本地开发用的脚本, 在本地 render HTML UI, 并在浏览器中打开预览, 直到你满意为止.

.. literalinclude:: ./liquid_render.py
   :language: python


3. 部署整个 Human Review Workflow
------------------------------------------------------------------------------

用 A2I as code script 部署 Task Template 以及 Flow definition. 最后运行 ``start_human_loop`` 函数, 触发 HIL, 然后 login 到 Workforce 的 UI 中 review 并 submit. 最后到 S3 bucket 中检查 Output.

.. literalinclude:: ./a2i_as_code.py
   :language: python
   :linenos:
