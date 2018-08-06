PyCharm Settings
==============================================================================

Use ``Ctrl + Alt + S`` (Windows) ``Cmd + ,`` (MacOS) to call settings.


Open File with Associated application
------------------------------------------------------------------------------

Editor -> File Types -> Files Opened in Associated Applications

For example, if you want to open ``*.rst`` with system application, then add ``*.rst`` to it.


Modify Python Editor Color Theme
------------------------------------------------------------------------------
Editor -> Colors & Fonts -> Python

- class def: bold pink
- bytes, string: light yellow
- comment: orange


Show White Space
------------------------------------------------------------------------------
``Preference`` -> ``Editor`` -> ``General`` -> ``Appearance`` -> check ``Show Whitespaces``.


Close AutoSave
------------------------------------------------------------------------------
I prefer to use

- Mark Unsaved Tabs: ``Preference`` -> ``Editor`` -> ``General`` -> ``Editor Tabs`` -> ``Mark Modified tabs with asterisk``
- Close Auto Save: ``Preference`` -> ``Appearance & Behavior`` -> ``System Settings`` -> ``Synchronization`` -> Uncheck ``Synchronize files on frame or editor tab activation``, ``Save files on frame deactivation``, ``Save files automatically if application is idle for xxx sec``.


Sync Setting
------------------------------------------------------------------------------
1. Create a repo on github, and create a token, give it ``repo`` rights.
2. Main menu -> File -> Settings Repository -> Paste the Git Url (example: https://github.com/<user-name>/<repo-name>.git -> Enter Token

Sync Setting:

- ``Overwrite Remote``: save your local setting to repo.
- ``Overwrite Local``: pull your cloud setting and overwrite local.

Tutorial: https://www.jetbrains.com/help/pycharm/sharing-your-ide-settings.html#settings-repository