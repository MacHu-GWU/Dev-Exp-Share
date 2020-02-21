return vs exit in function
==============================================================================

.. contents::


``return`` keyword
------------------------------------------------------------------------------

script:

.. code-block:: bash

    func() {
        echo "a"
        return
        echo "b"
    }

    func


output:

.. code-block:: bash

    a


``return`` status code
------------------------------------------------------------------------------

script:

.. code-block:: bash

    func() {
        return 99
    }

    func
    echo $?


output:

.. code-block:: bash

    99


``return`` can't return string
------------------------------------------------------------------------------
script:

.. code-block:: bash

    func() {
        return "a"
    }
    
    func

output:

.. code-block:: bash

    line 4: return: a: numeric argument required


use ``return`` to 'return' a string, method 1
------------------------------------------------------------------------------
Since function can't really return any argument, but we still have this trick.

script:

.. code-block:: bash

    func() {
        result="a"
    }
    
    func
    echo $result

output:

.. code-block:: bash

    a


**Becareful**:

.. code-block:: bash

    func() {
        echo "Hello"
        echo "World"
    }
    
    result=$(func)
    echo $result

output:

.. code-block:: bash

    Hello World


``exit`` in function, will kill the entire process
------------------------------------------------------------------------------
``exit`` is a system level command

``b.sh``:

.. code-block:: bash

    my_func() {
        echo "start my_func"
        exit 1
        echo "end my_func"          # will not be executed
    }


``a.sh``:

.. code-block:: bash

    source b.sh

    echo "start a.sh"

    my_func
    echo "exit code of my_func:" $? # will not be executed
    echo "end a.sh"                 # will not be executed


``main.sh``:

.. code-block:: bash

    bash a.sh
    echo "exit code of bash a.sh:" $?


output:

.. code-block:: bash

    start a.sh
    start my_func
    exit code of bash a.sh: 1
