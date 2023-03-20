
为什么我 SSH 进去在 bash 里打命令有用, 但同样的命令在 shell provisioner 里就没用?
------------------------------------------------------------------------------
Shell provisioner 用的是 ``/bin/sh``, 而不是 ``/bin/bash``. 在 Ubuntu 上 ``/bin/sh`` 是一种叫做 dash 的 shell (bash 的前身). 如果你要用 bash 来运行脚本, 你就不能用 inline, 而是要用 script, 然后在你的脚本第一行加上 ``!/bin/bash`` 的 shebang.

由于我们开发 packer 脚本的时候, 通常都是 SSH 进去先手动进行, 搞清楚了命令格式之后再放到 packer 脚本里. 可经常我们 SSH 进去的 shell 是 bash, 而 packer 用的是 ``/bin/sh``. 为了获得统一的开发体验, 我们可以用下面的语法::

    build {
      ...
      provisioner "shell" {
        script = "your_bash_script.sh"
      }
      ...
    }

而这个 ``your_bash_script`` 的第一行则是 ``#!/bin/bash``.

我个人喜欢用 python 写 shell script, 全面代替 bash. 但是 pyenv 却只在 bash 上安装了, ``/bin/sh`` 却找不到 pyenv. 为了解决这个问题, 我的 provisioner 是这样实现的::

    build {
      ...
      # 第一步先将 python 脚本相关的文件上传到服务器上
      provisioner "file" {
        source = "requirements.txt"
        destination = "/tmp/requirements.txt"
      }

      provisioner "file" {
        source = "your_python_script.py"
        destination = "/tmp/your_python_script.py"
      }

      # 然后用 bash 脚本来执行 python 脚本
      provisioner "shell" {
        script = "your_bash_script.sh"
      }
      ...
    }

其中 ``your_bash_script.sh`` 里的内容是:

.. code-block:: bash

    #!/bin/bash -e

    # 启用 pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    # 安装依赖
    pip3.8 install -r /tmp/requirements.txt

    # 运行脚本
    python3.8 /tmp/your_python_script.py

而如果你的工作不是一个脚本能搞定的. 那么你就需要再封装一层, 把 provisioner 里的 ``file`` 部分换层 ``git clone ...`` 从远端直接拉取一个仓库, 然后再在创建 virtualenv, 安装依赖, 用 virtualenv 里的 python 运行复杂脚本.

Reference:

- Troubleshooting Shell Provisioner: https://developer.hashicorp.com/packer/docs/provisioners/shell#troubleshooting