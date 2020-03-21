Cloud Migration (迁徙到云) Docs
==============================================================================

Reference:

- https://aws.amazon.com/blogs/enterprise-strategy/6-strategies-for-migrating-applications-to-the-cloud/

基本上有以下几种迁徙模式:

1. Rehost (life and shift), 对服务器的硬盘做 比特级 的复制, 然后再云上运行.
2. Replatform (lift-tinker-and-shift), 换一个平台, 例如将数据库从自家数据中心的虚拟机上迁徙到 AWS RDS 上.
3. Repurchasing, 购买新的产品, 例如抛弃过去的 CMS 员工管理系统, 使用 Salesforce.
4. Refactoring / Rearchitect, 重新设计架构, 例如从 monolithic 模式迁徙到 microservice 模式.
5. Retire
6. Retain

.. autotoctree::
    :maxdepth: 1
