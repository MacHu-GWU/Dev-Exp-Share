.. contents::

Execute
==============================================================================
- Run Last Executed File: ``Ctrl + R`` (MacOS)
- Select a file to Run: ``Ctrl + Alt + R`` (MacOS)


Set your Python executable (Even for virtualenv)
------------------------------------------------------------------------------
``Preference`` -> ``Project`` -> ``Project Interpreter``, Set Python executable.

Windows:

- ``C:\Python27\python.exe``

MacOS:

If your python are installed from `HomeBrew <https://brew.sh/>`_, it should be at:

- ``/usr/local/Cellar/python2/2.7.13/Frameworks/Python.framework/Versions/2.7/bin/python2.7

Linux:

- ``<path-to-your-virtualenv-folder>``


Set bash executable
------------------------------------------------------------------------------
Neet a `BashSupport <https://plugins.jetbrains.com/plugin/4230-bashsupport>`_ plugin.


Open File in Sublime Text
------------------------------------------------------------------------------
1. Set up external tools: ``Preference`` -> ``Tools`` -> ``External Tools`` -> ``Add new one`` click ``+`` sign.
2. Config executable: ``Name``: name for this tool, I use ``Sublime Text``, ``Description``: any description text, ``Program``: The executable file (.exe for Windows, Application/Sublime Text.app for MacOS), ``Parameters``: ``$FilePath$`` (you can select from macro), ``Working Directory``: ``$ProjectFileDir$``, click ``OK``.
3. Assign a Keymap: ``Preference`` -> ``Keymap`` -> Search ``Sublime Text`` -> Add a keymap, I use ``Shift + Cmd + S``.
4. Try it out: select a file in project view, press ``Shift + Cmd + S``.

- PyCharm: Open the current file in Vim, Emacs or Sublime Text: https://andrewbrookins.com/python/open-the-current-file-in-vim-emacs-or-sublime-text-from-pycharm/
