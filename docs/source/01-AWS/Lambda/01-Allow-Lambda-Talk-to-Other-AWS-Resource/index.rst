Allow Lambda Talk to Other AWS Resource
==============================================================================

设置:

- AWS Resource: 亚马逊的服务组件, 例如 EC2, RDS, Lambda.
- VPC (Virtual Private Cloud): 将一个 AWS Resource 放在某个虚拟的网络.
- Security Group: 为一个 AWS Resource 设置一组安全策略, 主要是针对数据在网咯上进出, Security Group 本身也可以放在某个 VPC 上, 也可以不用放在某个 VPC 上.

举个例子, 我们有个网站的 APP, 用到了这些组件:

- EC2, 作为服务器
- RDS, 作为数据库
- Lambda, 作为无服务器运算

通常, 我们会将不同的 AWS 资源放在不同的 VPC 网络之下. 一是为了方便控制, 二是为了安全, 一个被攻击了, 其他的不会受到影响. 我们用 vpc_ec2, vpc_rds, vpc_lambda 来表示.

那么, 我们也要为3个资源各配置一个 Security Group, sg_ec2, sg_rds, sg_lambda. 然后再 Inbound / Outbound 中把各自都加上即可.



Lambda talk to RDS
------------------


Lambda talk to S3
-----------------


Lambda talk to
--------------


