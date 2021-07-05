PyCharm Remote Development
==============================================================================

PyCharm 专业版 其中最为杀手级的功能可能要属 Remote Development 了. 他可以允许你


.. contents::
    :depth: 1
    :local:

Reference:

- https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html



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




