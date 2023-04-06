.. _setup-a-jump-box-ec2:

Setup A Jump Box EC2
==============================================================================

1. 在 Private Subnet 上启动一台 EC2, 我们假设这台机器是数据库服务器, 只允许从公网上访问. 我们称之为 DB Server.
2. 创建一个 Security Group (SG), 规则是 inbound 只允许从位于同一个 SG 的自己进行 ssh 连接. 你可以先创建这个 SG, 然后再添加 inbound rule. outbound 允许 all traffic to anywhere. 然后将这个 SG 指定给 DB Server. 这里的逻辑是, 给所有需要互相通信, 且位于 Private Subnet 上的机器都指定这个 SG. 而位于 Public Subnet 上的任意机器如果也有这个 SG, 则允许 ssh 连接.
3. 在 Public Subnet 上启动一台 EC2 作为 Jump Box. 创建一个新的 SG, 允许从限定的几个 IP, 比如你的家里, 工作场所的 WIFI, SSH 连接到该 Jump Box.
4. 将之前的 Private Subnet SG 也指定给 Jump Box, 所以 Jump Box 和 DB Server 拥有同一个 SG.
5. 为你的两台 EC2 配置 Key Pair, 可以使用不同的 Key, 也可以使用相同的 Key. 这里我们使用不同的 Key, Jump Box 使用 ``key1.pem``, DB Server 使用 ``key2.pem``.
6. 举例来说, Jump Box 的 ip 是 ``111.111.111.111``, DB Server 的内网 ip 是 ``222.222.222.222``, 你的个人电脑上的 Jump Box 的 pem key 的路径是 ``~/ec2-pem/key1.pem``, DB Server 的 pem key 的路径是 ``~/ec2-pem/key2.pem``, Jump Box 上你想要 pem key 位于 ``~/key2.pem``::


    # 首先将用于访问 DB Server 的 pem key 从本机拷贝到 Jump Box, 该操作只需要做一次
    scp -i ~/ec2-pem/key1.pem ~/ec2-pem/key2.pem ec2-user@111.111.111.111:~/key2.pem

    # 然后从你的个人电脑连接到 Jump Box
    ssh -i ~/ec2-pem/key1.pem ec2-user@111.111.111.111

    # 然后从 Jump Box 连接到 DB Server
    ssh -i ~/key2.pem ec2-user@222.222.222.222

    # 现在你已经在 DB Server 上了
