.. _zsh-root:

zsh The ZShell
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


注: 本文的所有内容均有自动化脚本实现自动安装, 请前往 https://github.com/MacHu-GWU/laptop/tree/master/home, 参考 ``configure-zsh.py`` 脚本.


Summary
------------------------------------------------------------------------------
zsh (Z Shell) 是 1990 年的一个项目, 只比 bash 的 1989 年晚一年出现. 发展了 30 年已经成为了事实上最强大, 社区生态最活跃, 插件最多的 shell. MacOS 在 2019-10-07 之后还让 zsh 成了系统默认的 shell. 跟 bash 的兼容性也很好. 非常适合作为开发者电脑上的 shell.


Install zsh
------------------------------------------------------------------------------
在 MacOS 从 Catalina 2019-10-07 以后 zsh 就取代了 bash 成为默认的 shell 了. 当然你也可以自己安装一个更高版本的. 具体可以参考下面的文档:

- Installing the Z Shell (zsh) on Linux, Mac OS X and Windows: https://gist.github.com/derhuerst/12a1558a4b408b3b2b6e
- ohmyzsh - installing ZSH: https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH

MacOS:

.. code-block:: bash

    brew install zsh

Linux - Ubuntu / Debians:

.. code-block:: bash

    apt install zsh

Linux - Centos / Redhat:

.. code-block:: bash

    sudo yum update && sudo yum -y install zsh


Install oh-my-zsh
------------------------------------------------------------------------------
``oh-my-zsh`` 是一个 zsh 的插件管理系统. zsh 的插件管理系统有很多, 但是 ``oh-my-zsh`` 可能是社区活跃度最高, 最流行, 配置最简单的.

- oh-my-zsh 官网: https://ohmyz.sh/


zsh Plugin System
------------------------------------------------------------------------------
zsh 有着强大的插件系统. 官网有个 GitHub Repo, 下面是 zsh 社区的各种插件: https://github.com/zsh-users.

如果你了解过 `fish shell <https://fishshell.com/>`_, 你会体会到 fish shell 的语法高亮, 自动补全的强大之处. 唯一的美中不足是 fish shell 毕竟是 2014 年的项目, 而 zsh 则是 1990 年的项目, 历史和 bash 一样悠久. 很多运维脚本都是用 bash 写的, 而用 fish 运行 bash 虽然大多数情况下没有问题, 只要你的 bash script 没有用到奇怪的语法. 而在生产环境中出现各种奇怪的问题是无法接受的. 这导致 fish 可能是大部分人的用来玩的开发脚本, 但不会用 fish 写自动化脚本. 如果你想要 fish shell 的这些语法高亮自动补全功能, 可以通过安装 zsh 插件来解决.

zsh plugin manager 有很多种, **但是大部分的 plugin 作者都建议优先使用源代码安装的方式**. 因为 plugin manager 的作者可能无法把所有的 zsh 插件都测试到, 所以不能保证 100% 稳定. 而大部分的 plugin 的作用方式都是把源代码 clone 到本地, 然后再用 source 的方式加载, 这种方式是完全可控的.


zsh Syntax Highlight Plugin
------------------------------------------------------------------------------
和 fish 类似的语法高亮. 绿色表示命令正确, 红色表示命令不正确.

- Plugin Homepage: https://github.com/zsh-users/zsh-syntax-highlighting


zsh Auto Suggestion Plugin
------------------------------------------------------------------------------
- Plugin Homepage: https://github.com/zsh-users/zsh-autosuggestions


zsh Auto Complete Plugin
------------------------------------------------------------------------------
zsh 的 autocomplete 插件堪称神器, 传统 shell 的补全跟 zsh 的智能补全完全没法比.

- Plugin Homepage: https://github.com/marlonrichert/zsh-autocomplete

启用这个插件后, 原先的 上下键 的功能就被修改了, 不再是上下查找历史命令. 这里有必要讲解一下该插件的快捷键操作的逻辑.

- Ctrl / Alt + Up 进入翻查命令历史记录菜单
- Ctrl / Alt + Down 进入 Auto Complete 的选项选择菜单
- 一旦进入多个选项的选择菜单:
    - Tab 是使用当前选择的选项 Auto Complete, 然后继续编辑命令
    - Shift Table 是使用最后一个可选的选项 Auto Complete, 然后继续编辑命令
    - Enter 是 Auto Complete, 然后立刻执行命令

- 在命令行没有输入任何命令的情况下:
    - Ctrl + Up 进入翻查历史命令菜单, 然后用 Up / Down 上下翻查命令, 然后用 Tab / Enter 进行下一步操作.
    - Ctrl / Alt + Down 进入下面的 auto complete 选择菜单, 然后用 上下左右 选择, 然后用 Tab / Enter 进行下一步操作.
    - Ctrl + R 进入搜索历史命令菜单, 优先展示最新的命令. 然后输入字符串搜索, 然后用 Ctrl / Alt + Down 进入下面的 搜索结果选择菜单, 然后用 Tab / Enter 进行下一步操作.
    - Ctrl + S 进入搜索历史命令菜单, 优先展示最老的命令. 和 Ctrl + R 类似.


zsh Keybinding
------------------------------------------------------------------------------
Keywords: zsh, key, keybinding, keymap, shortcut, 快捷键

zsh Shell 内置有一套快捷键绑定设置, 这套设置是可以在启动的时候在 ``~/.zshrc`` 修改.

- 查看目前已经绑定的快捷键: ``bindkey``
- 在当前的 session 绑定快捷键: ``bindkey '${keycode}' ${widget}``. 这里的 keycode 是虚拟 按键码. 你输入 ``cat -v`` 命令后, 然后按键盘上的按键即可出现对应的 虚拟按键码. widget 是内置命令或者由 plugin 实现的功能, 每个功能有一个对应名字. 例如默认设置下 ``bindkey '^[[A' up-line-or-history`` 意思就是 ``UP`` (方向键上) 的功能是光标向上移动或查看历史. 这里 ``^[[A`` 就是 ``UP`` 键的虚拟案件码.

- ``⌃ + u``: **清空当前行**
- ``⌃ + a``: **移动到行首**
- ``⌃ + e``: **移动到行尾**
- ``⌃ + f``: 向前移动 相当于 <-
- ``⌃ + b``: 向后移动 相当于 ->
- ``⌃ + p``: 翻看上一条命令 相当于 UP
- ``⌃ + n``: 翻看下一条命令 相当于 DOWN
- ``⌃ + r``: 搜索历史命令

- ``⌃ + y``: **召回最近用命令删除的文字**
- ``⌃ + h``: 删除光标之前的字符
- ``⌃ + d``: **删除光标所指的字符**
- ``⌃ + w``: **删除光标之前的单词**
- ``⌃ + k``: **删除从光标到行尾的内容**
- ``⌃ + t``: 交换光标和之前的字符


My Favorite Theme - powerlevel10k
------------------------------------------------------------------------------
`powerlevel10k <https://github.com/romkatv/powerlevel10k>`_ 可能是 zsh 最强大的主题了. 纵观这个代码库, star 达到了恐怖的 30K, 完成度极高, 自定义自由度极高.

- Installation: 因为这个主题要和 oh-my-zsh 配合使用, 所以参考 ``Installation -> Oh My Zsh`` 一节的文档, 将其安装在 ``~/.oh-my-zsh/custom/theme`` 目录下. 然后再在 ``.zshrc`` 中设置 ``ZSH_THEME="powerlevel10k/powerlevel10k"``
- Wizard: 第一次使用时会出现一个 configuration wizard, 问你一些问题然后自动生成 ``p10k`` 的配置文件, 该配置文件在 ``~/.p10k.zsh`` 处. 如果你对当前配置不满意, 你可以用 ``p10k configure`` 命令重新配置一遍.
- PyCharm Terminal Emoji Issue: Pycharm `有一个 Bug 会导致 PyCharm 自带的 Terminal emulator 无法显示 UTF-8 Emoji 图标 <https://youtrack.jetbrains.com/issue/IDEA-118832>`_. 解决方法是在 ``~/.zshrc`` 配置文件中添加 ``export LANG="en_US.UTF-8"`` 和 ``export LC_ALL="en_US.UTF-8"`` 两行, 使得 Shell 知道你的字符编码是 UTF-8. 然后在 PyCharm 上方的菜单里的 Help 菜单里选择 Edit Custom VM Option, 然后添加一行 ``-Dfile.encoding=UTF-8``, 这能告诉 Java VM 的字符编码为 UTF-8. 然后重启 PyCharm 后再进入 zsh 就能正常显示 Emojii 图标了.

Ref:

- Theme Homepage: https://github.com/romkatv/powerlevel10k
- Display Emojii in PyCharm Terminal: https://youtrack.jetbrains.com/issue/IDEA-118832


Add newline to Oh My ZSH Theme
------------------------------------------------------------------------------
有的 Theme (例如大名鼎鼎的 `agnoster <https://gist.github.com/agnoster/3712874>`_) 会显示完整的路径名, 这样会导致光标的起始位置不确定, 有时会在屏幕的很右边, 导致每次要去找这个光标.

下面这个回答提供了解决方案并解释了原理:

- StackOverFlow 回答: https://stackoverflow.com/questions/41017917/add-newline-to-oh-my-zsh-theme

简单来说是这样子的:

1. 在 ``~/.zshrc`` 文件中有一行是 ``source $ZSH/oh-my-zsh.sh`` 这行的功能是加载 ``~/.oh-my-zsh/themes/agnoster.zsh-theme`` 主题.
2. 主题文件里有一个函数 ``prompt_end()`` 定义了这个行为:

.. code-block:: bash

    # End the prompt, closing any open segments
    prompt_end() {
      if [[ -n $CURRENT_BG ]]; then
        echo -n " %{%k%F{$CURRENT_BG}%}$SEGMENT_SEPARATOR"
      else
        echo -n "%{%k%}"
      fi
      echo -n "%{%f%}"
      CURRENT_BG=''
    }

3. 我们要做的是在 ``~/.zshrc`` 文件中 ``source $ZSH/oh-my-zsh.sh`` 的后面覆盖这个函数, 将其替换为下面的函数. 其中唯一的变化是这一行 ``echo -n "\n$(date +"%Y-%m-%d %H:%M:%S%z") $%{%f%}"``, 等于我们在输入命令的前面先用 ``\n`` 换行, 然后再用 ``date`` 函数获得当前的时间.

.. code-block:: bash

    prompt_end() {
      if [[ -n $CURRENT_BG ]]; then
        echo -n " %{%k%F{$CURRENT_BG}%}$SEGMENT_SEPARATOR"
      else
        echo -n "%{%k%}"
      fi
      echo -n "\n$(date +"%Y-%m-%d %H:%M:%S%z") $%{%f%}"
      CURRENT_BG=''
    }

4. 之所以我们不直接修改 ``~/.oh-my-zsh/themes/agnoster.zsh-theme``, 是因为这个目录是你在安装 `oh-my-zsh <https://ohmyz.sh/>`_ 时安装的, 每次安装时候会覆盖这个, 而我们对 ``.zshrc`` 文件的控制权更多. 这样我们只需要维护 ``.zshrc`` 文件即可.

.. note::

    **该方法也适用于自定义其他 zsh 插件功能**
