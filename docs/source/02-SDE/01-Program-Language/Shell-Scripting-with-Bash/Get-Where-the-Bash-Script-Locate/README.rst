Get Where the Bash Script Locate
==============================================================================

在代码仓库中, 很多自定义的 shell script 需要根据工具所在的位置, 定位到其他文件并调用之. 那么只要你能够保证你的代码库的文件结构不变, 那么就能保证正常工作.

那么如何能够精准定位到 shell script 的当前目录呢?

.. code-block:: bash

    if [ -n "${BASH_SOURCE}" ]
    then
        dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    else
        dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
    fi
