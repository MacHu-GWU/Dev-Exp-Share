AWS Cloud9 Best Practice
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


连接到 Cloud 9 IDE
------------------------------------------------------------------------------
在 `创建 Cloud 9 Dev Environment Console 界面中 <https://console.aws.amazon.com/cloud9/home/create>`_ 有三种创建模式, 这决定了你如何连接到 Dev Environment, 很有必要说一下.

1. Create a new EC2 instance for environment (direct access): Launch a new instance in this region that your environment can access directly via SSH. 要求将 Cloud9 放在 Public Subnet 中. 这个的本质是通过 公网 IP, 然后在浏览器和 Cloud9 之间建立 SSH 连接. 除了用浏览器连接, 你还可以用 Terminal SSH 进去. 这种 Cloud9 和在 Public Subnet 上的 EC2 几乎没有区别.
2. Create a new no-ingress EC2 instance for environment (access via Systems Manager): Launch a new instance in this region that your environment can access through Systems Manager. 这种情况通常将 Cloud9 放在 Private Subnet 上. AWS System Manager 能创建一个临时的 credential, 让你从浏览器直接连接到 Cloud9 上. 你无法从公网直接 SSH 进去, 但可以通过位于同一个 VPC Public Subnet 上的 Jump host SSH 进去.
3. Create and run in remote server (SSH connection): Configure the secure connection to the remote server for your environment. 该选项没有 GUI, 只有 SSH 连接, 一般不使用.

**综上所述, 对于大型企业, 通常使用选项 2**. 因为大企业出于安全考虑, 一般不轻易把机器放在 Public Subnet 上.


自动关机
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
默认设置是 Dev Environment 超过 30 分钟没有任何动作 (点击 IDE, 输入命令行命令等) 就会 Stop EC2 Instance. 这样 EC2 就不收费了. 默认时间是 30 分钟, 你可以再 Cloud9 IDE Preference 界面 (小 Cloud9 云的那个 Icon) 中改动这个时间.

而你需要使用 Dev Environment 的时候点击 Open IDE 就会 Start EC2 Instance. 只要不是第一次启动, 这个启动时间通常在 30 秒 ~ 1 分钟.

有一个很 tricky 的问题是, 如果你有一个脚本需要运行超过 30 分钟, Cloud9 只会检测 IDE 是否有动静, 而不会监控是否有进程在运行, 所以可能会在你运行结束前就强行 Stop Instance.

目前只有两种解决方案:

1. 把关机时间延长到比如 4 小时, 保证足够运行了.
2. 设置为永不关机.


增加硬盘容量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AWS 提供了个脚本能改变当前主硬盘 EBS 的大小, 将下面的 shell script 保存为 ``resize-ebs.sh`` 然后 ``bash resize-ebs.sh 100`` 即可将硬盘扩容为 100GB. 可以通过查看 `官方文档 <https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize>`_ 获得这个脚本的最新版本.

参考资料:

- https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize


Cloud9 的 IAM 权限
------------------------------------------------------------------------------
Cloud9 本质上是一个 EC2. AWS 提供了两种方式管理对 AWS Service 操作的权限.

**第一种叫 AWS Managed Temporary Credentials**. 让你的 Cloud9 EC2 拥有跟环境创建者, 通常是 IAM User 相同的权限. 实际上是在 ``~/.aws/credential`` 和 ``~/.aws/config`` 处生成文件, 并隔一段时间就 rotate 一下具体的 Credential. 这个功能可以在 Cloud9 的 IDE 里的 Preference 里打开和关闭. 这是 AWS 最推荐的方式. 但是这有个限制, 你的 EC2 需要放在 Public Subnet 上.

.. warning::

    **如果你的 Cloud9 放在了 Private Subnet 上, 则无法使用 AWS Managed Temporary Credentials. 必须关闭这个选项并用 IAM Role 来控制权限**.

**第二种就是给 Cloud9 EC2 添加 IAM Role**. 记得要将第一种 AWS Managed Temporary Credentials 的设置在 IDE 里关闭才能生效. 默认情况下 Cloud9 会有一个自动创建的 ``AWSCloud9SSMAccessRole`` service role.

参考资料:

- Calling AWS services from an environment in AWS Cloud9: https://docs.aws.amazon.com/cloud9/latest/user-guide/credentials.html


Cloud9 + GitHub / GitLab / Code Commit
------------------------------------------------------------------------------
Cloud9 是一个云 IDE, 并不是一个 Remote Desk Top, 所有不能用下载 Git 图形化客户端软件. 但 Cloud9 原生支持 Git GUI, 虽然不是特别好用, 但是基本够用. 如果你的代码仓库是 host 在 GitHub / GitLab / CodeCommit 上, 可以参考下面的文档, 看如何与私有仓库交互.

- :ref:`use-aws-cloud9-with-github`
- :ref:`gitlab-authentication`
- :ref:`use-code-commit-repo-on-aws-cloud9-or-jupyter-lab`

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
