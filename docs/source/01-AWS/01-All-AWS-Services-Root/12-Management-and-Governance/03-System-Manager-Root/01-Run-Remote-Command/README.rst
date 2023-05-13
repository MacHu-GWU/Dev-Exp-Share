.. _run-remote-command-on-ec2-via-ssm:

Run Remote Command on EC2 via SSM
==============================================================================


Overview
------------------------------------------------------------------------------
在服务器上执行命令是一个非常普遍的需求. 通常我们有这么几种方法:

- SSH 登录服务器, 然后在终端里敲命令.
- 用远程执行工具, 例如 `paramiko <https://www.paramiko.org/>`_. 你需要管理好 SSH.
- 用 Ansible 一类的自动化工具.

AWS 原生的 System Manager 服务可以用来来执行远程命令. 这种方法的好处有很多:

- 无需管理 SSH.
- 使用 IAM Role 权限管理, 非常安全.
- 自动化程度高, 可以被嵌入或者编排成各种复杂的脚本.
- 可以和 AWS 的其他服务联动.

本文我们就来看看如何用 AWS 的 System Manager 来执行远程命令.


How it Work
------------------------------------------------------------------------------
AWS 有一个历史悠久的服务 SSM (System Manager), 该服务对标的是 Ansible 之类的服务器运维工具, 用于批量管理虚拟机. 和 Ansible 用 SSH 来执行远程命令的方式不同, SSM 是通过在机器上安装 SSM Agent (一个由 AWS 维护的系统服务软件), 然后让 SSM Agent 将自己自动注册到 SSM Fleet Manager, 然后通过 IAM 鉴权, 然后用 AWS 内部的 API 与 SSM Agent 通信从而执行远程命令.

我们来看一看在启动一台由 SSM 管理的 EC2 的过程中, 到底发生了什么:

- 启动机器, 启动操作系统以及系统服务, 其中系统服务就包括 SSM agent.
- SSM gent 启动后就会调用 IAM 的权限, 尝试将自己注册到 SSM Fleet Manager 上.
- 一旦注册成功, 你就可以用 SSM 来远程操纵 EC2 了.

从以上内容我们可以看出来, 安装 SSM Agent 至关重要. 所幸的事 `AWS 官方提供的一些 AMI <https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html>`_ (主要是 Amazon Linux) 上会预装 SSM Agent. 包括 AWS 认证过的第三方软件提供商例如 RedHat, Ubuntu 等公司提供的 AMI 也会预装 SSM Agent 并开机自动启动. 但是你用的是你自己或是 Market place 上的 AMI, 里面没有预装 SSM Agent, 你就需要自己安装了. 我们这个项目用的是 Ubuntu Server 20.04, 里面已经预装了 SSM Agent, 所以我们无需做任何额外工作.

在你启动 EC2 的时候 (包括启动新的 EC2, 或是 Stop 之后再 Start, 或是 Reboot 都可以, 因为只要启动系统服务就可以了), 只要你的 IAM Role 里有这个 由 AWS 管理的 IAM Policy ``arn:aws:iam::aws:policy/service-role/AmazonSSMManagedInstanceCore``, 或是你创建一个自己的 Policy 有同样的权限, 那么 SSM Agent 就会自动将自己注册到 SSM Fleet Manager. 虽然 Reference 中的官方文档用的 IAM Role 有特定的名字, 但其实什么名字都可以, 只要有对应的权限就可以.

Reference:

- SSM Agent 的官方文档: https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html


Manually Install SSM Agent on EC2
------------------------------------------------------------------------------
下面这些文档介绍了如何手动在 EC2 上安装 SSM Agent, 我并没有动手试过, 仅供参考.

- Linux: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html
- Windows: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-install-win.html
- MacOS: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install-macos2.html


一些有用的命令
------------------------------------------------------------------------------
你可以用 AWS CLI 来查看哪些 EC2 被注册到了 SSM 管理清单上, 你到 `SSM Fleet Manager Console <https://console.aws.amazon.com/systems-manager/managed-instances?>`_ 中看也是一样的:

.. code-block:: bash

    aws ssm describe-instance-information --output text --profile bmt_app_dev_us_east_1

你也可以 SSH 到 EC2 上运行如下命令来检查 SSM Agent 是否已经启用 (该项目基于 ubuntu server 20.04, 其他系统请参考 `官方文档 <https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html#verify-ssm-agent-status>`_):

.. code-block:: bash

    sudo systemctl status snap.amazon-ssm-agent.amazon-ssm-agent.service


用 SSM Agent 执行远程命令
------------------------------------------------------------------------------
下面这段代码展示了如何用 boto3 SDK 通过 SSM 运行远程命令.

.. literalinclude:: ./example.py
   :language: python
   :linenos:

有了概念之后, 我们来看一个更高级的模块, 适用于生产环境的代码:

.. literalinclude:: ./ssm_remote_command.py
   :language: python
   :linenos:

Reference:

- 用 SSM 远程执行命令的官方教程: https://aws.amazon.com/getting-started/hands-on/remotely-run-commands-ec2-instance-systems-manager/
- 发送命令的 Python API 文档: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command


总结
------------------------------------------------------------------------------
1. 在创建 EC2 之前就要配置好你的 IAM Role.
2. 确保你给 EC2 的 IAM Role 有这个 ``AmazonSSMManagedInstanceCore`` IAM Policy.
3. 启动 EC2 的时候使用这个 IAM Role. 如果启动的时候忘记给 IAM Role, 那么你可以启动后指定 IAM Role 然后重启即可.
4. 然后就可以用 SSM 的 API 来远程执行命令了.


Remote Command 还能用来干什么
------------------------------------------------------------------------------
很多自动化脚本由于网络连接的缘故是必须要在 EC2 上运行的. 所以我们可以在世界的任意地点用 SSM agent 来执行远程命令. 而而关于传输数据, 我建议通过 S3 做媒介, 让 EC2 将命令执行后的数据写入到 S3 上. 这样你就可以在任意地点读取这些数据了.
