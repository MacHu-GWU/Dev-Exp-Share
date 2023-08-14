Setup AWS Managed SFTP Server
==============================================================================


1. Overview
------------------------------------------------------------------------------
本文介绍了如何在 AWS 上搭建一个全托管的 SFTP 服务器.

首先我们来了解一下背景信息. 用 SSH 连接到远程服务器是一个历史超级悠久的技术了. SFTP (Secure File Transfer Protocol) 是一个基于 SSH 技术的, 把远程服务器的磁盘当做文件服务器的网络通信协议. 该技术通常需要自己管理一个服务器, 并且在服务器上部署一个 SFTP server 监听 22 号端口, 即可为外界提供服务了. SFTP server 本质上跟 Web Server 没什么大的区别.

我们自己架设并管理一个稳定, 安全的 SFTP server 其实很复杂, 要考虑很多问题, 例如网络安全, 访问权限, 秘钥管理, 数据备份, 服务器扩容. 通常你要付出一个人工成本和硬件成本, 这是一笔不小的开支. 市场上其实也有服务提供商能托管一个 SFTP server, 但这本质是帮你托管一台虚拟机并定期帮你备份硬盘, 很多问题还是需要你自己解决.

AWS 作为世界上最大的云服务提供商, 于 2018 年上线了全托管式的 SFTP 服务. 提供了更高级的, 可自定义的权限管理, 服务扩容, 以及数据可用性. 接下来我们就来看看如何使用 AWS SFTP 服务.


2. What is AWS Transfer
------------------------------------------------------------------------------
AWS Transfer 是一个 AWS 全托管的 business to business file transfer 的服务, 而 AWS managed SFTP server 只是它的一个功能, 除此之外还有很多例如 workflow 等更高级的功能. 它提供了 SFTP 等一众常见的文件传输服务器的全托管服务. 不仅如此, 它还提供了丰富的鉴权方式和后端存储的方式.

鉴权方式有这些, 除了 SSH 之外, 能更加方便的跟企业中常用的其他登录方式集成:

- SSH
- Directory
- Custom identity provider

后端存储方式除了用服务器本机存储以外, 还有 S3, EFS 等这些云原生, 高可用, 高扩展, 数据安全有保障的后端存储:

- S3
- EFS


3. When should I use AWS Managed SFTP server
------------------------------------------------------------------------------
本节讨论一下什么时候我们考虑使用 AWS Managed SFTP server.

首先, 你都上云了, 你用 SFTP 服务器的目的肯定不是自己内部用. 内部用有 S3 等许多更好的方案. 如 AWS Transfer 的描述 "business to business file transfer" 所说, 它是一个为不同企业之间传输文件而设计的服务. 例如当你需要将文件提供给别人, 让别人定期到这里来下载文件, 或是别人需要将文件提供给你, 它就是一个很好的选择. 因为你是在 AWS 云上, 但别人不一定在云上, 也不一定有 AWS 的开发者经验, 特别是你的合作方是比较传统的企业, 对 SFTP, SSH 比较熟悉的时候, 用 SFTP 作为媒介传输数据就很合适.


4. AWS Transfer SFTP Pricing
------------------------------------------------------------------------------
本节我们来看一下使用 AWS Managed SFTP server 的成本.

使用全托管的服务降低了维护服务器的人力成本, 以及保障了服务和数据的可用性. AWS Managed SFTP Server 有两个部分的费用:

- 每个 Protocol 每小时 0.3$ 的固定费用
- 上传和下载都是每 GB 0.04$ 的费用

这样算来每个月固定成本就是 0.3 * 24 * 30 = 216$. 我认为跟雇一个运维人员的费用, 以及面临丢失数据的风险, 这个价格并不贵.

Reference:

- `AWS Transfer Family pricing <https://aws.amazon.com/aws-transfer-family/pricing/>`_


5. Create a AWS Managed SFTP Server
------------------------------------------------------------------------------
本节介绍了创建一个 AWS Managed SFTP server 的具体步骤.

**创建 SFTP 服务器**

进入 `AWS Transfer Console <https://console.aws.amazon.com/transfer/home#/servers>`_, 在左边菜单选择 ``Servers``, 然后点击位于右上的 ``Create server`` 按钮, 进入创建 SFTP server 的页面.

- Choose protocols: 选择 ``SFTP (SSH File Transfer Protocol) - file transfer over Secure Shell``, 开起 SFTP 服务. 你可以同时开启多个 Protocol, 但我们这个例子里只用到了 SFTP.
- Choose an identity provider: 选择 ``Service managed``, 由自己创建用户并管理登录.
- Choose an endpoint: 选择 ``Publicly accessible``. 如果你要限制特定的网络段才能访问你的 SFTP 服务器, 你就要用 ``VPC hosted`` 并为其配置 Security Group.
- Domain: 选择 ``Amazon S3`` 或者 ``Amazon EFS``. 这里我们选择 ``Amazon S3`` 作为后端存储.
- Configure additional details:
    - CloudWatch logging: logging role 选择 ``New role``, 除非你知道怎么创建这个 Role. 这个 Role 就是用来将服务器日志写到 CloudWatch log 中的.
    - Cryptographic algorithm options: 这是密码算法协议版本, 你用默认的就好.
    - Server Host Key: 这个是用来从已经存在的 SFTP Server migrate 到 AWS 的时候用的. 你如果不是 migrate 就不用管这个.
    - 其他都用默认

**在 SFTP 服务器上添加一个 User**

然后就可以点击你刚创建的 Server, 往下拉找到 ``Add user`` 按钮, 为你的服务器添加一个受信用户.

- User configuration: 输入一个用户名, 这个用户名将会在你用 SSH 连接的时候用到.
- Role 和 Policy: 这里非常有必要详细解释一下. 你会看到 Role 和 Policy 两个需要定义的选项. 有 AWS 经验的人就会觉得奇怪, Role 里面不是已经定义了 Policy 了吗? 怎么还有一个 Policy? 这里的鉴权的方式是当 Policy 不是 None 的时候, IAM Role 和 Policy 都要有权限. 而 Policy 是 None 的时候 IAM Role 有权限即可. 这里的 Role 像是一个物理机器上的 Role, 而 Policy 则是每个 SSH 连接 Session 的权限. 我比较推荐的做法是给这个 Role 对于特定的 bucket 的读写权限. 然后 Policy 选择 "Auto-generate policy based on home folder". 这个 Policy 能将 User 的读写权限进一步的限制在它自己的 ``${HOME}/${username}/`` 下.

这个 Role 的 trusted entities policy 是:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "transfer.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

这个 Role 的 inline policy 是:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:GetObjectTagging",
                    "s3:GetObjectVersion",
                    "s3:PutObject",
                    "s3:PutObjectTagging",
                    "s3:PutObjectVersionTagging",
                    "s3:DeleteObject",
                    "s3:DeleteObjectTagging"
                ],
                "Resource": [
                    "arn:aws:s3:::${your-bucket-name}",
                    "arn:aws:s3:::${your-bucket-name}/*"
                ]
            }
        ]
    }

- Home directory 你选择一个 Bucket 就好.
- SSH public key: 这里简单介绍一下 RSA 非对称加密算法. 本质上你只要把 Public Key 给服务器, 然后你在服务器通信的时候服务器会自动把服务器的 Public Key 给你, 于是双方都有自己的 Private Key 以及对方的 Public Key, 就可以通信了. 我建议你用 ``ssh-keygen`` 命令生成一对 RSA key, 并将 Private key 保存在 AWS Secret manager 上. 然后把 Public Key 保存在任何地方都可以. 这里你需要将 SSH public key 的内容 (用任意文本编辑器打开) 填进去, 这样才能用这个 User 跟服务器通信. 对于同一个用户你可以添加多个 Public Key, 这个在你成功创建了 User 之后可以进行修改.

至此, 你已经创建了一个 AWS managed SFTP server, 并且使用了高可用的 S3 存储以满足无线扩容的需求. 下一节我们将介绍如何在 Python 中编写程序对 SFTP 进行读写.

Reference:

- `Create an SFTP-enabled server <https://docs.aws.amazon.com/transfer/latest/userguide/create-server-sftp.html>`_
- `Working with service-managed users <https://docs.aws.amazon.com/transfer/latest/userguide/service-managed-users.html>`_


6. Read / Write to SFTP in Python
------------------------------------------------------------------------------
这里我们使用 `paramiko <https://pypi.org/project/paramiko/>`_ 库来进行 SFTP 的读写. 这是一个历史非常悠久, 非常成熟的 SSH 库, 可以放心使用.

.. literalinclude:: ./example.py
   :language: python
   :linenos:
