Sagemaker Notebook Instance
==============================================================================
Keywords: Sagemaker Notebook Python Version

Summary
------------------------------------------------------------------------------



Jupyter Lab Version, Available Kernel and Python version
------------------------------------------------------------------------------
一个 Notebook Instance 上运行的 Jupyter Lab 版本和 Available Kernel 是在启动 Notebook Instance 的时候选择 Platform identifier 的时候决定的. 而 Python version 则是由 Kernel 决定的.

目前支持的 Platform identifier 有这些. 其中 al1, 2 是指的 Amazon Linux 1 和 2 (底层的 Linux AMI) 具体有什么 Kernel 的信息可以看 `这篇文档 <https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-al2.html>`_:

- Amazon Linux 1, Jupyter Lab 1, notebook-al1-v1
- Amazon Linux 2, Jupyter Lab 1, notebook-al2-v1
- Amazon Linux 2, Jupyter Lab 3, notebook-al2-v2


Install External Libraries
------------------------------------------------------------------------------
Kernel 自带的包很可能无法满足你开发的需求, 那么你就需要额外安装一些包. 在 Jupyter Notebook 中有两种特殊命令: 以 ``%`` 开头的 magic command, 和以 ``!`` 开头的 shell command. ``%`` 只支持 ``%conda`` 和 ``%pip``. 而 ``!`` 支持任何 shell command.


Link
------------------------------------------------------------------------------

- Use Amazon SageMaker Notebook Instances: https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html
- Amazon Linux 2 vs Amazon Linux notebook instances: https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-al2.html
- JupyterLab versioning: https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-jl.html
- Install External Libraries and Kernels in Notebook Instances: https://docs.aws.amazon.com/sagemaker/latest/dg/nbi-add-external.html
