Set Environment Variable in Child Script
==============================================================================


Parent Bash Script use Variable in Child Bash Script
------------------------------------------------------------------------------

很多时候我们有一个脚本设置了一些环境变量, 或仅仅就是一些变量. 然后我们希望从另外一个脚本 "import" 这些变量, 或是使用这些环境变量.

举例, 我们有一个脚本 ``child.sh`` 里面定义了一个环境变量 ``TEST_VAR``, 我们希望在主脚本 ``main.sh`` 中使用这个环境变量. 正确的做法是 ``source ./child.sh`` 或是 ``. ./child.sh``.

Child::

    #!/bin/bash

    TEST_VAR="this is test var" # ``export TEST_VAR="this is test var"`` also works

Parent::

    #!/bin/bash

    source child.sh # this doesn't work: ``bash child.sh``
    echo $TEST_VAR


Parent Bash Script use Variable in Child Python Script
------------------------------------------------------------------------------

我们希望能在 Bash Script 中执行一个 Python 脚本, 然后这个 Python 脚本设定一些环境变量, 然后执行完之后再在 Bash Script 使用这些环境变量. 就像下面的例子:

Python::

    # -*- coding: utf-8 -*-
    # content of child.py

    import os
    os.environ["TEST_VAR"] = "this is a testvar"

Bash Script::

    #!/bin/bash
    # content of main.sh

    python child.py
    echo $TEST_VAR # expect to see: this is a testvar

先说结论:

    **这是不可能的**, 因为 ``python child.py`` 命令本身是一个 sub process, 子进程 是无法修改父进程中的环境变量的.

    **但你可以让 Python 将一些变量的值以某种方式, 或是通过 stdout, 文件, 等方式返回给 Bash Script. 这需要额外的工作**.

一个例子:

Python::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import os
    import json

    if __name__ == "__main__":
        os.environ["TEST_VAR"] = "this is test var"

        data = {"TEST_VAR": os.environ["TEST_VAR"]}
        print(json.dumps(data))

Bash Script::

    #!/bin/bash

    python_output_data=$(python child.py)
    TEST_VAR=$(echo $python_output_data | jq '.TEST_VAR' -r)
    echo $TEST_VAR
