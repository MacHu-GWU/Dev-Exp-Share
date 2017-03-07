Config Python Interpreter
===============================================================================

You may need to run a script in python2 or python3, so you have to set up a default build system for Sublime, then you can use Ctrl + B to run your script.

First, edit or create a config file at::

	C:\Users\your-username\AppData\Roaming\Sublime Text 3\Packages\User\python27.sublime-build
	C:\Users\your-username\AppData\Roaming\Sublime Text 3\Packages\User\python34.sublime-build

Here's how to create a python27 and python34 system: Menu -> Tools -> Build System -> New Build System, add this json to the configuration file.

::

	// Windows For Python27
	{
		"cmd": ["C:\\python27\\python.exe", "-u", "$file"],
		"encoding": "utf8" // 这样才能打印中文
	}

::

	// Windows For Python34
	{
		"cmd": ["C:\\python34\\python.exe", "-u", "$file"],
		"encoding": "cp936" // 这样才能打印中文
	}

::

	// Ubuntu For Python27
	{
		"shell_cmd": "/usr/bin/env python2 ${file}",
		"encoding": "utf8" // 这样才能打印中文
	}

::

	// Ubuntu For Python34
	{
		"shell_cmd": "/usr/bin/env python3 ${file}",
		"encoding": "utf8" // 这样才能打印中文
	}

How to choose your default interpreter?

1. Alt + T (access tool menu)
2. Alt + U (access build system)
3. choose your system
4. Once you have chosen a interpreter, then you can call Ctrl+B to build and run it