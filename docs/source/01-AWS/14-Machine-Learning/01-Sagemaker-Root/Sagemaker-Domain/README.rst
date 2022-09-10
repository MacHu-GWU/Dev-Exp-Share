Sagemaker Domain
==============================================================================
一个 SM Domain 就是一个 ML 的环境.

一个 Domain 下有如下资源.

1. 一个 EFS 文件系统
2. 一堆 Authorized User
3. 一堆 Security Policy
4. 一个 VPC

一个 AWS Account 的一个 Region 只能有一个 SM Domain. 在这个 Domain 的 内部, 你可以 Share notebook 和文件以及其他的 Artifacts

UserProfile: A user profile represents a single user within a Domain, and is the main way to reference a user for the purposes of sharing, reporting, and other user-oriented features. This entity is created when a user onboards to the Amazon SageMaker Domain.

App: An app represents an application that supports the reading and execution experience of the user’s notebooks, terminals, and consoles. The type of app can be JupyterServer, KernelGateway, RStudioServerPro, or RSession. A user may have multiple Apps active simultaneously.

The following tables describe the status values for the Domain, UserProfile, and App entities. Where applicable, they also give troubleshooting steps.



- 一个 Domain 就是