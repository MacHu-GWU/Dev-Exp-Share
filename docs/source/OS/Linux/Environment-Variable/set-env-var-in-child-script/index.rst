Set Environment Variable in Child Script
==============================================================================

很多时候我们有一个脚本设置了一些环境变量, 或仅仅就是一些变量. 然后我们希望从另外一个脚本 "import" 这些变量, 或是使用这些环境变量.

举例, 我们有一个脚本 ``child.sh`` 里面定义了一个环境变量 ``TEST_VAR``, 我们希望在主脚本 ``main.sh`` 中使用这个环境变量. 正确的做法是 ``source ./child.sh`` 或是 ``. ./child.sh``.

.. code-block:: bash

    #!/bin/bash
    # content of child.sh

    export TEST_VAR="this is test var"


.. code-block:: bash

    #!/bin/bash
    # content of main.sh

    . ./child.sh # it works
    # bash child.sh # not work
    # ./child.py # not work

    echo $TEST_VAR
