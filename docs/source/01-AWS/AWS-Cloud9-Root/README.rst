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


Cloud9 Runner
------------------------------------------------------------------------------

Runner 就是当你选中一个文件, 点击 Run (或用快捷键) 时, 实际发生的 Command Line 命令.

例如系统自带的 python3.7 对应着 ``python3.7 $filename`` 这个命令, 其中 $filename 是你当前选中文件相对与当前所在目录的相对路径.

如果你要用其他 Python, 比如 virtualenv 里的 Python 来运行, 那么你就要定义一个 virtualenv 专用的 Runner file. Runner file 就是一个 Json 文件. 你在 cmd 里把第一个命令定义为 virtualenv 中的 Python 所在路径即可.

.. code-block:: javascript

    // Create a custom Cloud9 runner - similar to the Sublime build system
    // For more information see http://docs.aws.amazon.com/console/cloud9/create-run-config
    {
        "cmd" : ["/home/ec2-user/environment/venv/bin/python", "$file", "$args"],
        "info" : "Started $project_path$file_name",
        "env" : {},
        "selector" : "source.py"
    }

然后你点击 python 文件, 然后点击 Run. 在右边有个 ``Runner``. 如果它没有自动发现你刚才配置的 Runner, 你可以手动选择, 然后点击左边的 Run 按钮即可.
