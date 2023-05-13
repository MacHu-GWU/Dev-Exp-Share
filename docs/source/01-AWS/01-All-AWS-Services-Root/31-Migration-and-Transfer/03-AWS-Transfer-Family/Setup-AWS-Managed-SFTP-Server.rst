Setup AWS Managed SFTP Server
==============================================================================


Overview
------------------------------------------------------------------------------
用 SSH 连接到远程服务器是一个历史超级悠久的技术了. SFTP (Secure File Transfer Protocol) 是一个基于 SSH 技术的, 把远程服务器的磁盘当做文件服务器的网络通信协议. 该技术通常需要自己管理一个服务器, 并且在服务器上部署一个 SFTP server 监听 22 号端口, 即可为外界提供服务了. SFTP server 本质上跟 Web Server 没什么大的区别.

我们自己假设并管理一个稳定, 安全的 SFTP server 其实很复杂, 要考虑很多问题. 那有没有一种办法能够让我们不用管理服务器, 也不用管理 SFTP server, 就能够拥有自己的 SFTP server 呢? AWS Transfer 就提供了这个服务.


What is AWS Transfer
------------------------------------------------------------------------------
AWS Transfer 是一个 AWS 全托管的 business to business file transfer 的服务, 它提供了 SFTP 等一众常见的文件传输服务器的全托管服务. 不仅如此, 它还提供了丰富的鉴权方式和后端存储的方式.

鉴权方式有这些, 除了 SSH 之外, 能更加方便的跟企业中常用的其他登录方式集成:

- SSH
- Directory
- Custom identity provider

后端存储方式除了用服务器本机存储以外, 还有 S3, EFS 等这些云原生, 高可用, 高扩展, 数据安全有保障的后端存储:

- S3
- EFS


AWS Transfer SFTP Pricing
------------------------------------------------------------------------------
使用全托管的服务免去了维护服务器的人力成本以及保障了服务和数据的可用性, 代价就是要给 AWS 付钱. AWS Managed SFTP Server 有两个部分的费用:

- 每个 Protocol 每小时 0.3$ 的固定费用
- 上传和下载都是每 GB 0.04$ 的费用

这样算来每个月固定成本就是 0.3 * 24 * 30 = 216$. 但我认为跟数据可用性, 和雇人维护的成本相比, 这个价格还是很划算的.

Reference:

- `AWS Transfer Family pricing <https://aws.amazon.com/aws-transfer-family/pricing/>`_


Create a AWS Managed SFTP Server
------------------------------------------------------------------------------
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

然后就可以点击你刚创建的 Server, 往下拉找到 ``Add user`` 按钮, 为你的服务器添加一个受信用户.

- User configuration: 输入一个用户名, 这个用户名将会在你用 SSH 连接的时候用到.
- Role: 每一个用户都会绑定一个 IAM Role 权限. 由于我们这个例子中是用 S3 作为后端存储, 那么这个用户必须要有对应的 IAM 权限才能访问到数据, 提供了双层保险. 本质上当用户发起请求时, Server 会自动 assume 这个 Role, 然后再去访问 S3.

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

IAM Role Policy 我们直接用了 AWS 提供的 ``AmazonS3FullAccess``. 这个 Policy 里面包含了 S3 所有的权限, 你可以根据自己的需求来定制这个 Policy.

然后下面还有一个 Policy, 最好选择 ``Auto-generate policy based on home folder``. 因为 Server 上的文件系统是跟 S3 Bucket 对应的, 每个用户 SSH 登录的时候有一个 username, 对应的是 S3 里面的 ``${HOME}/${username}`` 这个目录. 如果你选择 None, 那么这个 User 就会用 IAM Role 上的权限来访问 S3. 而如果打开了 ``Auto-generate policy based on home folder``, 则会自动将用户的访问权限限制在 ``${HOME}/${username}`` 这个目录下. 这时候建议你不要给 IAM Role 里任何权限. 比如你 IAM Role 里给了 ``AmazonS3FullAccess``, 那么这一设置就形同虚设了. 不过为了测试方便, 我们还是用的 ``AmazonS3FullAccess`` + None 的设置.

- Home directory 你选择一个 Bucket 就好.
- SSH public key: 这里简单介绍一下 RSA 非对称加密算法. 本质上你只要把 Public Key 给服务器, 然后你在服务器通信的时候服务器会自动把服务器的 Public Key 给你, 于是双方都有自己的 Private Key 以及对方的 Public Key, 就可以通信了. 我建议你用 ``ssh-keygen`` 命令生成一对 RSA key, 并将 Private key 保存在 AWS Secret manager 上. 然后把 Public Key 保存在任何地方都可以. 这里你需要将 SSH public key 填进去, 这样才能用这个 User 跟服务器通信. 对于同一个用户你可以添加多个 Public Key, 这个在你成功创建了 User 之后可以进行修改.

Reference:

- `Create an SFTP-enabled server <https://docs.aws.amazon.com/transfer/latest/userguide/create-server-sftp.html>`_
- `Working with service-managed users <https://docs.aws.amazon.com/transfer/latest/userguide/service-managed-users.html>`_

