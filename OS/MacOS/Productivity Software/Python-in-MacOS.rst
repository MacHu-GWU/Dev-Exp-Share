Python in MacOS
==============================================================================
Mac系统虽然自带Python，但是专业的Python开发者会同时需要Python2，3甚至更多版本。


Install Multiple Python Version
------------------------------------------------------------------------------

Don't Use ``brew install python2``, ``brew install python3``; Use ``pyenv`` instead. Because brew doesn't have full versions.

``pyenv`` lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

install pyenv: ``brew install pyenv``。

``~`` is user home directory.

- All python versions will be installed in: ``~/.pyenv/versions``.
- bash profile file: ``~/.bash_profile``.

- List all available version: ``pyenv install -l``.
- Install specified version: ``pyenv install <version>``.
- Switch to specified python version: ``pyenv global/local/shell <version>``.
- Check current version: ``pyenv version``.
- Check all installed version: ``pyenv versions``.

If you have a preference order, you can define the order this way: ``pyenv global 2.7.13 3.4.6 3.5.3 3.6.2``.

    Every time after installed a new python version, run ``pyenv rehash``

ref:

- document: https://github.com/pyenv/pyenv
- installation: https://github.com/pyenv/pyenv#installation
- `pyenv Command <https://github.com/pyenv/pyenv/blob/master/COMMANDS.md>`_
