AWS Cloud9
==============================================================================

Cloud9 是一个位于云端的 Linux 开发机器. 产品定位是给那些 budget 有限, 不能给 Developer 配 MacBook. 而是给开发者比较差的电脑, 然后用基于 EC2 的 Cloud9 进行开发. 不用的时候关闭, 用的时候打开.

.. contents::
    :depth: 1
    :local:



Cloud9 本体功能
------------------------------------------------------------------------------



自动关机
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认设置是 当 IDE 开启时 Start Instance, 当 IDE 关闭一定时间或者没有输入后 Stop Instance. 默认时间是 30 分钟, 你可以再 Cloud9 IDE Preference 界面中改动这个时间.

有一个很 tricky 的问题是, 如果你有一个脚本需要运行超过 30 分钟, Cloud9 只会检测 IDE 是否有动静, 而不会监控是否有进程在运行, 所以可能会在你运行结束前就强行 Stop Instance.

目前只有两种解决方案:

1. 把关机时间延长到比如 4 小时, 保证足够运行了.
2. 设置为永不关机.


增加硬盘容量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS 提供了个脚本能改变当前主硬盘 EBS 的大小, 将下面的 shell script 保存为 ``resize-ebs.sh`` 然后 ``bash resize-ebs.sh 100`` 即可将硬盘扩容为 100GB.

.. code-block:: bash

    #!/bin/bash
    #content of resize-ebs.sh

    # Specify the desired volume size in GiB as a command-line argument. If not specified, default to 20 GiB.
    SIZE=${1:-20}

    # Get the ID of the environment host Amazon EC2 instance.
    INSTANCEID=$(curl http://169.254.169.254/latest/meta-data/instance-id)

    # Get the ID of the Amazon EBS volume associated with the instance.
    VOLUMEID=$(aws ec2 describe-instances \
      --instance-id $INSTANCEID \
      --query "Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId" \
      --output text)

    # Resize the EBS volume.
    aws ec2 modify-volume --volume-id $VOLUMEID --size $SIZE

    # Wait for the resize to finish.
    while [ \
      "$(aws ec2 describe-volumes-modifications \
        --volume-id $VOLUMEID \
        --filters Name=modification-state,Values="optimizing","completed" \
        --query "length(VolumesModifications)"\
        --output text)" != "1" ]; do
    sleep 1
    done

    #Check if we're on an NVMe filesystem
    if [ $(readlink -f /dev/xvda) = "/dev/xvda" ]
    then
      # Rewrite the partition table so that the partition takes up all the space that it can.
      sudo growpart /dev/xvda 1

      # Expand the size of the file system.
      # Check if we are on AL2
      STR=$(cat /etc/os-release)
      SUB="VERSION_ID=\"2\""
      if [[ "$STR" == *"$SUB"* ]]
      then
        sudo xfs_growfs -d /
      else
        sudo resize2fs /dev/xvda1
      fi

    else
      # Rewrite the partition table so that the partition takes up all the space that it can.
      sudo growpart /dev/nvme0n1 1

      # Expand the size of the file system.
      # Check if we're on AL2
      STR=$(cat /etc/os-release)
      SUB="VERSION_ID=\"2\""
      if [[ "$STR" == *"$SUB"* ]]
      then
        sudo xfs_growfs -d /
      else
        sudo resize2fs /dev/nvme0n1p1
      fi
    fi


参考资料:

- https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize


Cloud9 使用 AWS Service 的权限
------------------------------------------------------------------------------

Cloud9 本质上是一个 EC2. AWS 提供了两种方式管理对 AWS Service 操作的权限.

第一种叫 AWS Managed Temporary Credentials. 让你的 Cloud9 EC2 拥有跟环境创建者, 通常是 IAM User 相同的权限. 实际上是在 ~/.aws/credential 和 ~/.aws/config 处生成文件, 并隔一段时间就 rotate 一下具体的 Credential. 这个功能可以在 Cloud9 的 IDE 里的 Preference 里打开和关闭. 这是 AWS 最推荐的方式.

第二种就是给 Cloud9 EC2 添加 IAM Role. 记得要将第一种 AWS Managed Temporary Credentials 的设置在 IDE 里关闭才能生效.

参考资料:

- Calling AWS services from an environment in AWS Cloud9: https://docs.aws.amazon.com/cloud9/latest/user-guide/credentials.html


Cloud9 + GitHub
------------------------------------------------------------------------------

Cloud9 是一个云 IDE, 并不是一个 RDP, 所有不能用图形化客户端软件, 在 Cloud9 上只能用 git 命令行.

AWS 官方推荐使用 Personal Access Token 用于 GitHub Authorization. 对于私有仓库, Clone 时你要输入 Username 和 Token. 对于任何仓库你 Push 时也要输入.

Cloud9 环境下常用 git 命令::

    git clone
    git clone --branch ${branch_name}
    git branch --list
    git branch ${branch_name}
    git diff
    git diff --name-only
    git add
    git add --all
    git commit -m "commit message"
    git push
