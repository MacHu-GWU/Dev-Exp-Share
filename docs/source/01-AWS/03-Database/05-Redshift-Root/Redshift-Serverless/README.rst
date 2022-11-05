.. _redshift-serverless:

Redshift Serverless
==============================================================================


Summary
------------------------------------------------------------------------------

NameSpaces Workgroups
------------------------------------------------------------------------------
因为 Redshift Serverlss 是无服务器的, 也就不存在具体的服务器的管理了. 而只有 Schema / Table / User 等. 你怎么能对其进行管理呢?

这就引入了 Namespaces 和 Workgroups 的概念. Namespaces 就是对数据相关的资源进行管理的. 而 Workgroup 是负责对计算资源进行管理的, 例如 RPU, VPC 等.

Namespace is a collection of database objects and users. The storage-related namespace groups together schemas, tables, users, or AWS Key Management Service keys for encrypting data. Storage properties include the database name and password of the admin user, permissions, and encryption and security. Other resources that are grouped under namespaces include datashares, recovery points, and usage limits. You can configure these storage properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs for the specific resource.

Workgroup is a collection of compute resources. The compute-related workgroup groups together compute resources like RPUs, VPC subnet groups, and security groups. Properties for the workgroup include network and security settings. Other resources that are grouped under workgroups include access and usage limits. You can configure these compute properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs.

You can create one or more namespaces and workgroups. A namespace can exist without any workgroup associated with it. Each namespace can have only one workgroup associated with it. Conversely, each workgroup can be associated with only one namespace.

Ref:

- Overview of Amazon Redshift Serverless workgroups and namespaces: https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-workgroup-namespace.html

Redshift Serverless vs Redshift
------------------------------------------------------------------------------




Reference
------------------------------------------------------------------------------
- Amazon Redshift Serverless: https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html
- Amazon Redshift Serverless is now generally available (2022-07): https://aws.amazon.com/about-aws/whats-new/2022/07/amazon-redshift-serverless-generally-available/


- Amazon Redshift Serverless Technical Overview Deck: https://aws.highspot.com/items/62a8d0a5282f1e220bf892bb?lfrm=srp.4
- Amazon Redshift Serverless - First Call Deck: https://aws.highspot.com/items/62ccc8244585166b17aa16a1?lfrm=srp.2