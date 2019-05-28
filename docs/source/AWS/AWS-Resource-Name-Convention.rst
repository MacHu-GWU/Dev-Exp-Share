VPC
---

- **VPC Name**: ``<vpc_name>``, example: ``default``. VPC Spans all the Availability Zone, so there's no need to include az information in the name
- **Subnet Name**: ``<vpc_name>/<private_or_public><serial_num_1,2,3>/<az>``, example: ``default/private1/us-east-1a``. We need to know the purpose and the az information in the subnet name.
- **Route Table Name**: ``<vpc_name>/<main_or_secondary>/<usage_name>``, example: ``default/main/private``. We need to know if it is a main route table or its usage.
- **NAT Gateway**: ``<vpc_name>``. Usually on VPC only need one NAT Gateway for all Private Subnet.
- **Security Group**:
    - No VPC: ``<purpose>``.
    - with VPC: ``<vpc_name>/<purpose>``.


Lambda
------

- Function Name: ``<service_name>-<stage>-<function_name>``: Lambda 是微服务架构的一部分. 通常情况下一个微服务包含多个 Lambda 函数. 所以, 用服务名 ``<service_name>`` 来区分函数是一个不错的选择.


IAM Role Name
-------------

- Role Name: ``<resource_name>-<granted_access>``



S3 Bucket
---------
S3 Bucket Name: