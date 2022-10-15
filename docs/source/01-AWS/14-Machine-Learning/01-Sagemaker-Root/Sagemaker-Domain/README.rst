Sagemaker Domain, Studio and Canvas
==============================================================================
Keywords: Sagemaker, Domain, Studio, Canvas

对于数据科学家和数据分析师来说, 杀手应用是 Jupyter Notebook. 而 AWS Sagemaker 的杀手应用则是 Studio, 一个 AWS 基于 Jupyter Lab 进行二次开发的 IDE 环境. 界面跟 Jupyter Lab 非常类似.

这几个东西经常放在一起讲, 我们先来对其做一个简单区分:

1. Domain

    一个 SM Domain 就是一堆对用户不可见的 网络, 文件系统, 虚拟机 等实体资源. 而你的 ML 开发环境, 脚本存储等都需要在上面运行. 一个 SM Domain 下有如下资源.

    1. 一个 EFS 文件系统
    2. 一堆 Authorized User
    3. 一堆 Security Policy
    4. 一个 VPC

    一个 AWS Account 的一个 Region 只能有一个 SM Domain. 在这个 Domain 的 内部, 你可以 Share notebook 和文件以及其他的 Artifacts. 一个 Domain 下可以有很多 UserProfile 和 App. 一个 UserProfile 就代表了一个 IAM Role, 你要使用 App 就得 assume 一个 UserProfile. 而这个 UserProfile 的 IAM 权限决定了他进入 App 之后能干什么.

    参考资料:

    - Onboard to Amazon SageMaker Domain: https://docs.aws.amazon.com/sagemaker/latest/dg/gs-studio-onboard.html

2. Studio

    是你的 ML 开发的 IDE. 背后是在 Domain 上的某台机器运行着的 Jupyter Lab. 要运行 Studio 你要先选择 UserProfile 然后点 Launch App, 然后就会自动选择 Domain 上的某台机器运行 Jupyter Lab, 并且自动连接上 EFS 上的文件数据.

3. RStudio

    我没有研究, 估计是 R 语言对应着的环境

4. Canvas

    是 AWS 开发的一个 low code ML 的环境, 让用户不写 Code 也能构建 ML 模型


参考资料
------------------------------------------------------------------------------
- Amazon SageMaker Machine Learning Environments 详细介绍了 Domain, Studio, RStudio, Canvas 等概念和用法: https://docs.aws.amazon.com/sagemaker/latest/dg/domain.html