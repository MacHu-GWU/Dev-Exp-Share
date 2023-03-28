Run Remote Command
------------------------------------------------------------------------------
keywords: aws system manager run remote command on ec2

在服务器上执行命令是一个非常普遍的需求. 通常我们有这么几种方法:

1. SSH 登录服务器, 然后在终端里敲命令.
2. 用远程执行工具, 例如 `paramiko <https://www.paramiko.org/>`_. 你需要管理好 SSH.
3. 用 Ansible 一类的自动化工具.

本文介绍了一种在 AWS 上用 System Manager 来远程执行命令的方法. 这种方法的好处是自动化程度高, 可以被嵌入或者编排成各种复杂的脚本.

AWS 有一个历史悠久的服务 SSM (System Manager). 你在启动 EC2 的时候, 如果给其配备的 IAM Role 里包含这个由 AWS 管理的 IAM Policy ``arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM``, 那么 EC2 会自动安装 SSM Agent. 这个 Agent 就能允许你在 AWS Console 或是用 SSM API 在 EC2 上远程执行命令. 当然这些命令都是被异步执行的.

请看一段 Python 代码的例子:

.. literalinclude:: ./example.py
   :language: python

总结下来就是:

1. 在创建 EC2 之前就要配置好你的 IAM Role
2. 确保你给 EC2 的 IAM Role 有这个 ``AmazonEC2RoleforSSM`` IAM Policy
3. 启动 EC2 的时候使用这个 IAM Role
4. 然后就可以用 SSM 的 API 来远程执行命令了

参考资料:

- 用 SSM 远程执行命令的官方教程: https://aws.amazon.com/getting-started/hands-on/remotely-run-commands-ec2-instance-systems-manager/
- 发送命令的 Python API 文档: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command