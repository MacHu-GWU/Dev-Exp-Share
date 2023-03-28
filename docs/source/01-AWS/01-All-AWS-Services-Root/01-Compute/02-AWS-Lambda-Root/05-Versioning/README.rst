

本文主要探讨 在使用 AWS Lambda 作为微服务时候的版本发布运维问题.

简单来说

第一个版本上线:

1. 开发第一个版本, 部署到 Lambda
2. 然后创建一个新的 Version, 叫做 v1.
3. 创建 3 个 Alias 分别叫做 Dev / Test / Prod. 目前所有的 Alias 都指向 v1.
4. 把 Lambda 的消费者指向 Alias Prod.

开发第二个版本:

1. 开发第二个版本, 在本地进行充分测试
2. 部署到第二个 Lambda.