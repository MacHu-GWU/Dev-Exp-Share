Get Where the Bash Script Locate
==============================================================================

.. code-block:: bash

    if [ -n "${BASH_SOURCE}" ]
    then
        dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    else
        dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
    fi
