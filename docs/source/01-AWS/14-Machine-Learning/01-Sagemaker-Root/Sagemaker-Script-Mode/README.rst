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