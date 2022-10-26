.. _ssh-to-aws-cloud9:

SSH To AWS Cloud9
==============================================================================
如果你自己在本地有一个 SSH Key Pair, 你想用这个 Key Pair 直接 SSH 到 Cloud9 上, 该怎么做?

前提:

你用的是 ``ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`` 这种方式在本地生成了 ``id_rsa`` (私钥) 和 ``id_rsa.pub`` (公钥), 或是参照 `GitHub 文档 <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_ 中的方式生成的.

Cloud 9 有三种 Launch 方式

- Choose **Create a new EC2 instance for environment (direct access)** to connect to the new environment from a newly launched Amazon EC2 instance.
- Choose **Create a new no-ingress EC2 instance for environment (access via Systems Manager)** to connect to the new environment from an Amazon EC2 instance without opening inbound ports.
- Choose **Create and run in remote server (SSH connection)** to connect to the new environment from your own server.

我们一个一个来讨论.


Direct Access
------------------------------------------------------------------------------
这时 Cloud9 本质上就是一个新创建的 EC2. 你先要用 Cloud9 IDE 登录进去, 然后找到 ``~/.ssh/authorized_keys`` 文件用 vi 打开, 然后将你的 公钥添加到这个文件中即可. 所谓添加就是在这个文件里另起一行, 然后把你的公钥内容拷贝进去, 整个公钥的内容就是一行, 以 ssh-rsa 起头 (取决于你的加密算法), 你的 email 结尾. 看起来像这样::

    # 一堆已经有的公钥

    # 你新添加的公钥
    ssh-rsa ABCDEF1234= your_email@example.com

详细做法请参考 AWS `Add or remove Key Pair <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/replacing-key-pair.html>`_ 文档.

然后你就可以用 ``ssh -i "~/.ssh/id_rsa" ec2-user@111.112.113.114`` 这样的 ssh 命令连接到 Cloud9 了.
