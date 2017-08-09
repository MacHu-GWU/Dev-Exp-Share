.. contents::

Config Python Interpreter
===============================================================================

You may need to run a script in python2 or python3, so you have to set up a default build system for Sublime, then you can use Ctrl + B to run your script.

First, edit or create a config file at::

    C:\Users\your-username\AppData\Roaming\Sublime Text 3\Packages\User\python27.sublime-build
    C:\Users\your-username\AppData\Roaming\Sublime Text 3\Packages\User\python34.sublime-build

Here's how to create a python27 and python34 system: Menu -> Tools -> Build System -> New Build System, add this json to the configuration file.


Windows Python 2
------------------------------------------------------------------------------

.. code-block:: javascript

    // Windows For Python27
    {
        "cmd": ["C:\\python27\\python.exe", "-u", "$file"],
        "encoding": "utf8", // 这样才能在控制台打印中文
    }

Windows Python 3
------------------------------------------------------------------------------

.. code-block:: javascript

    // Windows For Python34
    {
        "cmd": ["C:\\python34\\python.exe", "-u", "$file"],
        "encoding": "cp936", // 这样才能在控制台打印中文
    }


Mac Python 2
------------------------------------------------------------------------------

.. code-block:: javascript

    // MacOS For Python34
    {
        "cmd": ["/usr/local/Cellar/python/2.7.13_1/Frameworks/Python.framework/Versions/2.7/bin/python2.7", "-u", "$file"],
        "env": {"LANG": "en_US.UTF-8"}, // 这样才能在控制台打印中文
    }


Mac Python 3
------------------------------------------------------------------------------

.. code-block:: javascript

    // MacOS For Python34
    {
        "cmd": ["/usr/local/Cellar/python3/3.4.4/Frameworks/Python.framework/Versions/3.4/bin/python3.4", "-u", "$file"],
        "env": {"LANG": "en_US.UTF-8"}, // 这样才能在控制台打印中文
    }


Ubuntu Python 2
------------------------------------------------------------------------------

.. code-block:: javascript

    // Ubuntu For Python27
    {
        "shell_cmd": "/usr/bin/env python2 ${file}",
        "encoding": "utf8", // 这样才能在控制台打印中文
    }

Ubuntu Python 3
------------------------------------------------------------------------------

.. code-block:: javascript

    // Ubuntu For Python34
    {
        "shell_cmd": "/usr/bin/env python3 ${file}",
        "encoding": "utf8", // 这样才能在控制台打印中文
    }


How to choose your default interpreter?
------------------------------------------------------------------------------
1. Alt + T (access tool menu)
2. Alt + U (access build system)
3. choose your system
4. Once you have chosen a interpreter, then you can call Ctrl+B to build and run it