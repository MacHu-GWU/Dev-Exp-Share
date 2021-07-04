Connect to Private Subnet RDS via Jump Host using SQL Client
==============================================================================

开发和测试环境的数据库往往无需那么严格的安全配置. 为了优先方便和效率, 往往会将 RDS 部署到 Public Subnet 并允许 Public Access. 然后为 RDS 的 Security Group 配置只允许从开发者本地机器所在网络访问. 这已经相当安全了. 等于说你要身处 特定网络, 有账号和密码 才能访问. 而作为开发者, 只要身处特定网络, 有账号密码, 既可以像连接本地机器上的数据一样连接 RDS.

而在生产环境中, RDS 都被部署在了 Private Subnet, 并只允许从位于 Public Subnet 上的 App 服务器访问, 通常 App 服务器都有配置 Security Group, 而 Database 的 Security Group 会只允许从 App 服务器的 Security Group 进行访问. 而 App 服务器本身也是被 Security Group 保护的, 而且藏在 Load Balancer 之后.

企业中通常只允许特定开发者直接从本地电脑连接位于生产环境的数据库, 比如 DBA, 运维人员, 只读调试等.

**下面, 我们来介绍两种连接位于 Private Subnet 的数据库的方式**:

1. 用带 GUI 的 SQL Client 例如 DBeaver, Microsoft Workbench, Jetbrain Data Grib
2. 用编程语言中的 SQL Client 例如 Python + Sqlalchemy

**架构**: Local PC <---> Jumpbox (Public Subnet) <---> RDS Instance (Private Subnet)

Jumpbox 是一台位于 Public Subnet 的 EC2.

**前提**: Jumpbox 的 Security Group 要打开 ssh 22 号端口给 本地开发机器所在网络的 IP. RDS Instance 的 Security Group 要打开 TCP $PORT (取决于你的数据库类型, mysql 是 3306, postgres 是 5432 等) 给 Public Subnet 所在的 CIDR, 更严格一点, 只给 Jumpbox 所在的 Security Group Id 打开.

1. 使用 Dbeaver 客户端连接数据库:

- 点击小插头图标, 创建新的连接:
- 选择数据库类型
- 填入 host, port, database, username, password
- 点击 Next, 进入 Network Setting
- 勾选 Use SSH Tunnel
- 在 Host/IP 填入你的的 Jumpbox Public IP, Port 填 22 (是 SSH 的默认端口)
- 在 Username 填入 Linux 默认用户, AmazonLinux 和 Redhat 是 ``ec2-user``, Ubuntu 是 ``ubuntu``
- Authentication Method 选择 Public Key, 在 Private Key 处选择 Jumpbox 所用的 ``*.pem`` Key 文件.
- 点击 Next, 进入 General
- 给 Connection 一个有意意的名字.
- 完成.

2. 使用编程语言的 SQL Client 连接数据库, 我们这里以 Python + Sqlalchemy 为例:

- 在 Mac 命令行填入下面的命令, 其功能是用创建一个 SSH Tunnel: ``ssh -i ${path-to-your-pem-file} -f -N -L ${local_port_for_db_connect}:${rds_endpoint}:${rds_port} ${linux_username}@${jumpbox_public-ip} -v``. 简单来说你凡是发给 localhost:{local_port_for_db_connect} 的数据, 会通过 jumpbox, 转发到 {rds_endpoint}:{rds_port}, 也就是数据库.
- 在 Sqlalchemy 中填写的 host 和 port 分别是 127.0.0.1 或 localhost, 以及 ``${local_port_for_db_connect}``. 其他 database, username, password 不变.
- 可以用该 Linux 命令列出处于连接状态的 ssh 连接列表: ``sudo lsof -i -n | egrep '\<ssh\>'``, 其中第二列是 pid. 你可以用命令 ``kill ${pid}`` 来杀死 ssh tunnel 进程.

参考资料:

- How can I connect to my Amazon RDS DB instance using a bastion host from my Linux/macOS machine?: https://aws.amazon.com/premiumsupport/knowledge-center/rds-connect-using-bastion-host-linux/
