Set Environment Variable for Subsequent Script
==============================================================================
Keywords: Environment Variable, shell script, python script.

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


定义问题
------------------------------------------------------------------------------
有一个 ``main.py`` 脚本, 功能是打印 ``EnvName`` 环境变量.

.. code-block:: python

    # -*- coding: utf-8 -*-
    # content of main.py

    import os

    print(os.environ.get("EnvName"))

我们知道如果在 ``main.py`` 代码中加入 ``os.environ["EnvName"] = "local"`` 就可以在运行 Python 程序的时候设置.

但有的时候你这个 ``main.py`` 是一系列 bash command 中的一环, 你不能修改这个 ``main.py``, 你希望在运行这个之前对环境变量进行设置, 并期待在 ``main.py`` 内部被捕获到. 这应该怎么做呢?


方法 1, 在 terminal 中修改环境变量
------------------------------------------------------------------------------
.. code-block:: bash

    $ export EnvName="local" # 注意, EnvName="local" 只是为你的当前 shell session 的上下文设置了一个变量. 而这不是环境变量.
    $ python main.py
    local


方法 2, 在 shell script 中修改环境变量
------------------------------------------------------------------------------
.. code-block:: bash

    #!/bin/bash
    # content of run.sh

    export EnvName="local"
    python main.py


方法 3, 在 python shell script 中修改环境变量
------------------------------------------------------------------------------
.. code-block:: python

    # -*- coding: utf-8 -*-
    # content of run.py

    import os
    import subprocess

    os.environ["EnvName"] = "local"
    subprocess.call(["python", "main.py"])
