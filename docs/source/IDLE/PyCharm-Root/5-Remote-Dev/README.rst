PyCharm Remote Development
==============================================================================

PyCharm 专业版 其中最为杀手级的功能可能要属 Remote Development 了. 他可以允许你将代码实时同步到远程服务器上, 并用远程服务器上的 Python 或是 Bash 一键用快捷键执行. 能在本地编辑代码库, 同时直接能看到远程服务器的文件目录.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Reference:

- https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html

理解远程开发
------------------------------------------------------------------------------

远程开发的应用场景以及需求:

场景:

平时开发者的代码是在本地机器上运行, 而远程开发则是让代码在远程服务器上运行. 而服务器上通常没有本地机器上的一整套开发工具链, 开发效率会大打折扣. 而且将代码同步到远程机器上并执行这个操作本身并不像在本地开发一个快捷键就搞定这么简单. 打断了开发者的思维节奏, 降低了效率.

在远程服务器上运行代码的原因通常常有:

1. 直接在生产环境, 或在跟生产环境类似的环境中进行调试. 帮助解决生产环境中出现的问题, 或是在更接近于生产环境中的计算资源中测试.
2. 远程服务器有本地开发机器所没有的 计算, 存储, 文件 等资源, 或是 网络 和 API 的权限.

需求:

1. 在本地编辑代码, 同时将代码库的改动实时自动或是手动同步到远程服务器上.
2. 使用远程服务器上的 程序运行代码. 包括编程语言或是 shell script.
3. 将远程执行的结果反映到本地.

PyCharm 的远程开发原理:

PyCharm 主要通过插件实现的远程开发功能. 原理上是在本地和远程服务器建立 SSH 连接, 然后在两者之间同步文件. 将本地快捷键所执行的命令行映射到远程机器上执行.


使用远程开发 1. 准备工作
------------------------------------------------------------------------------

在此文档中, 我们以 MacOS 作为本地开发机器, AWS Amazon Linux EC2 作为远程服务器. 使用 ``.pem`` 秘钥文件作为 SSH 连接的钥匙.

1. 在 AWS 上创建一台 EC2.
2. 确保你给 EC2 指定了 Key, 并下载了 Key (一个 ``.pem``) 文件.
3. 然后给其配置合适的 Security Group, 允许从你的 IP SSH 连接.
4. 然后确保他在 Public Subnet 上并有 Public Ip.


远程执行 Python 以及文件同步
------------------------------------------------------------------------------

设置 SSH 连接:

1. 进入菜单 ``Tools -> SSH Configuration``. 右边菜单分 两栏, 左边是配置好的 SSH 连接列表, 右边是选中的连接配置的详细信息.
2. ``Host`` 填 EC2 的 Public Ip, ``Port`` 填 22, ``Authentication Type`` 选择 Key Pair, ``Private Key`` 选择你的 ``.pem`` 文件的绝对路径.
3. 最后给配置好的 SSH Configuration 一个名字, 建议用 ``${AWS_ACCOUNT_ALIAS}/${EC2_NAME}`` 这样的格式. 你一看就知道这个机器是在哪个 AWS Account 上叫什么名字.

设置 Remote Interpreter:

1. 进入菜单 ``Project: ${你的项目名称} -> Python Interpreter``
2. 点击右边菜单里的 ``Python Interpreter`` 右边的齿轮, 选择 Add. 然后选择 SSH Interpreter.
3. 在 ``Existing Server Configuration`` 中选择你之前创建好的 SSH Configuration. 然后点击 Next.
4. ``Interpreter`` 里填的是你的解释器的绝对路径. 即使在远程环境中, 我们也仍然推荐使用 virtualenv 创建一个虚拟环境来安装依赖和运行 Python.
5. ``Sync Folder`` 里天的是你要把本项目的文件所同步到的目录的路径. 我建议在一个项目中约定一个惯例. 比如 Git Repo 叫做 MY_PROJECT, 那么远程的同步路径就用 ``/tmp/pycharm-projects/MY_PROJECT``.

至此, 我们的远程 Python 解释器已经配置完成.

远程执行 Bash / Shell Script
------------------------------------------------------------------------------

编辑要在服务器上运行的 Bash 脚本的工作通常是先 SSH 到服务器上, 然后用 Vim 编辑后回到 Shell 中运行. 有些人会在本地机器编辑好然后通过 SCP, FTP, Git 同步到远程服务器上执行.

PyCharm 专业版的加持下, 工作流变成了, 在本地编辑好 Bash Script, 保存直接按快捷键在远程服务器上执行. 这样的使得效率提高了不止一点半点. 而且可以在有语法高亮, 代码检查功能的编辑器中编写脚本. 下面我来介绍一下怎么配置.

在专业版中的工具分类下会多出很多选项, 其中跟远程执行 Shell Script 相关的是 ``Remote SSH External Tools``.

1. ``Cmd + ,`` 打开设置菜单 ``Tools -> Remote SSH External Tools``
2. 给这个 Tool 一个名字, 比如在 ``Name`` 框里填入 ``Run Bash Remotely``.
3. 在 Tool Settings 中按如下填写, 该含义是: 先 CD 到 Working Directory, 然后再输入 ``${Program} ${Argument}`` 这样的命令. 其中 Working Directory 中的 ``$ProjectName$`` 是该项目文件夹的名字, ``$FileRelativeDir$`` 是 .sh 文件的文件夹之于项目文件夹的相对路径. 简单来说就是 CD 到 .sh 文件所在的文件夹下. 而之前的 ``/tmp/pycharm-projects`` 则是跟你的配置 ``Python Interpreter`` 时候所指定的 ``Path Mappings`` 相关. 我个人习惯是将项目文件夹 Map 到远程服务器上的 ``/tmp/pycharm-project/$ProjectName$`` 处. 所以我们这样配置能将 Working Directory 指定到 .sh 文件所在的文件夹下:
    - Program: /bin/bash
    - Arguments: $FileName
    - Working Directory: /tmp/pycharm-projects/$ProjectName$/$FileRelativeDir$
4. 在 Connect Settings -> SSH Configuration 中选择你的服务器所用的 Configuration. 这一设置是告诉 PyCharm 如何 SSH 到远程服务器上的. 你每次换了远程服务器后, 需要更新这一设置.
5. 最后, 你在 Keymap 菜单里, 搜索你刚才创建的 Remote SSH External Tools 的名字 ``Run Bash Remotely`` 然后给一个快捷键, 我的设置是 Alt + ` (反撇) (相应滴直接用 Bash 的快捷键是 Shift + ` (反撇).


远程服务器文件浏览器以及文件同步
------------------------------------------------------------------------------

总的来说, 当你指定了 Path Mapping 之后, PyCharm 会将任何写入到磁盘的改动 Upload 同步到服务器上. 你在本地修改完然后立刻执行, 就是最新的结果.

但是仍然有些情况, 比如你手动在服务器上对文件夹下的文件进行了改动, 或是删除了文件夹, 那么同步会偶尔失效. 所以我们需要掌握手动同步并重置 PyCharm 同步器的技巧.

在菜单 ``Tools -> Deployment`` 下的选项通常都是跟同步相关, 有上传, 有下载, 还有一个远程服务器文件浏览器 ``Browse Remote Host``.




