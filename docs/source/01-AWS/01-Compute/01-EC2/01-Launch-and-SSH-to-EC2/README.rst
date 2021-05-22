Launch and SSH to EC2
==============================================================================

本文内容:

- 启动 EC2 虚拟机
- SSH 连接至 EC2


Step1. Launch EC2
------------------------------------------------------------------------------

本质上 EC2 就是使用 虚拟机软件, 例如 VMWare, 在亚马逊的数据中心上运行的虚拟机. 虚拟机主要作为服务器使用, 这里面 90% 以上的服务器是 Linux.



Step2. Connect via SSH
------------------------------------------------------------------------------

Grant access to your pem key:

.. code-block:: bash

    chmod 400 ~/ec2-pem/<key-pair-name>.pem

SSH connect:

.. code-block:: bash

    $ ssh -i {path-to-your-pem-file} {username}@{ip-address}

- ``path-to-your-pem-file``: it is where you store your EC2 SSH Key Pair ``.pem`` file, usually, you should put it at ``${HOME}/ec2-pem/<key-pair-name>.pem``
- ``username``: the operation system username account. By default, if it is Amazon Linux, it is ``ec2-user``. If it is ubuntu, it is ``ubuntu``. It is not your IAM username!
- ``ip-address``: For EC2 on public subnet, public IPV4 address, can be found at your EC2 instances dashboard. For EC2 on private subnet, it is private IPV4 address.

Reference:

- Connecting to Your Linux Instance Using SSH: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
- Transferring Files to Linux Instances from Linux Using SCP


Step3. Connect via SSH the Better Way
------------------------------------------------------------------------------

由于在我们启动一个 EC2 的时候, 是并不知道他的 public ip 地址的. 而每次 EC2 关闭再启动后, 这个 IP 地址都会改变. 我们希望提供一小段代码, 使得每次想要 SSH 到 EC2 上的时候, 只要快速的复制粘贴即可.

.. code-block:: bash

    # specify your ec2 name
    EC2_NAME="your-ec2-name"

    # specify your cli profile
    AWS_PROFILE="your-aws-cli-profile"

    # retrieve public ip
    EC2_IP="$(aws ec2 describe-instances --filters "Name=tag:Name,Values=${EC2_NAME}" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text --profile ${AWS_PROFILE})"

    # retrieve private ip
    EC2_IP="$(aws ec2 describe-instances --filters "Name=tag:Name,Values=${EC2_NAME}" --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text --profile ${AWS_PROFILE})"

    # specify the default user, for redhat, centos, amazon linux, it is ec2-user. for ubuntu it is ubuntu
    EC2_USER="ec2-user"

    # specify the location of your pem file
    EC2_PEM="path-to-your-pem-file"

    # run ssh connect
    echo EC2_PEM="${EC2_PEM}", EC2_USER="${EC2_USER}", EC2_IP="${EC2_IP}" && ssh -i ${EC2_PEM} ${EC2_USER}@${EC2_IP}


Step4. Copy file or dir between EC2 and local machine via SSH Copy
------------------------------------------------------------------------------

Reference:

- Linux – How to Securely Copy Files Using SCP examples: https://haydenjames.io/linux-securely-copy-files-using-scp/

.. code-block:: bash

    # Copy file from a EC2 to local host:
    $ scp -i {path-to-your-pem-file} <username>@<ec2-ip>:<path-to-ec2-file> <path-to-file>

    # Copy file from local host to a EC2:
    $ scp -i {path-to-your-pem-file} <path-to-file> <username>@<ec2-ip>:<path-to-ec2-file>


    # Copy directory from a EC2 to local host:
    $ scp -i {path-to-your-pem-file} -r <username>@<ec2-ip>:<path-to-ec2-dir> <path-to-dir>

    # Copy directory from local host to a EC2:
    $ scp -i {path-to-your-pem-file} -r <path-to-dir> <username>@<ec2-ip>:<path-to-ec2-dir>
