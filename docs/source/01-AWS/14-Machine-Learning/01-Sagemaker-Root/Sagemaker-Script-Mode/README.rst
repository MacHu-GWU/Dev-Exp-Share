Sagemaker Script Mode
==============================================================================


介绍
------------------------------------------------------------------------------
根据前面的知识我们知道 Sagemaker 的杀手级功能就是把 "用远程服务器训练机器学习模型" 这一功能封装好了. 但是使用这一功能的前提是你所用的算法 Sagemaker 有预先配好的的 AMI 和 Docker Image 环境. 这些复杂的工作是 AWS 在维护. 但是社区不断的涌现各种新算法, 很多算法你是无法直接用 Sagemaker SDK 中直接远程执行的. 所以 Sagemaker SDK 提供了 Script Mode 这一功能, 能让 Data Scientist 免于复杂的构建运行环境镜像的麻烦, 而专注于撰写 training 代码.

为了帮助理解, 你可以看下面的对比:

- 目的是用高性能大内存的远程服务器来训练 ML 模型
- 什么工具都不用, 硬写 Notebook: 自己写 script, 自己构建 Runtime
- 用 Sagemaker Training: 不用写 script, 不用构建 Runtime, 只用填 parameter
- 用 Sagemaker Script Mode: 自己写 script, 不用构建 Runtime

Script Mode 的核心是 entry point script, 跟 docker 里的 entry point script 类似.


文档
------------------------------------------------------------------------------
- 介绍 Script Mode 的概念以及提供了一些示例代码: https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-script-mode/sagemaker-script-mode.html
    - 一个 entry point 的例子: https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-script-mode/scikitlearn_script/train_deploy_scikitlearn_without_dependencies.py
- 一个使用 Script Mode + Sklearn 的例子: https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-script-mode/sklearn/sklearn_byom_outputs.html
    - 一个 entry point 的例子: https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-script-mode/sklearn/train.py
- 一个介绍 Script Mode 的 AWS Blog: https://aws.amazon.com/blogs/machine-learning/bring-your-own-model-with-amazon-sagemaker-script-mode/


如何编写 Training Script
------------------------------------------------------------------------------

- 如何编写 Training Script 的官方文档: https://sagemaker.readthedocs.io/en/stable/frameworks/sklearn/using_sklearn.html#preparing-the-scikit-learn-training-script


如何在不 Build Docker Image 的情况下的在 Script Mode 中使用额外的 Python Library
------------------------------------------------------------------------------
**问题**

    我们在 Jupyter Notebook 上开发了一个 ML 模型. 但是在开发的过程中我们需要用 ``%pip install ...`` 安装了一些第三方依赖. 而我的 ML 模型需要用到这些依赖. 我们如何在 Remote Training 以及 Deploy Endpoint 的时候包含这些依赖呢?

**分析问题的本质**

    我们用 Sklearn 举例. Script Mode 的本质就是 Sagemaker 自己管理着一个 Docker Container. 里面安装了 Python 以及一些 Sklearn 的依赖. 而你本地的 Jupyter Notebook 的 Kernel 里也有一些依赖. 这个问题的本质就是找到 AWS Managed Docker Container 和你开发用的 Jupyter Notebook 中的依赖列表的差异.

    这个差异

