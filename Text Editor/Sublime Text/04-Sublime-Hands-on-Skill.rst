.. contents::

Sublime Hands On Skill
==============================================================================


Windows下快捷键汇总
------------------------------------------------------------------------------
**Mac** 下基本上是将 ``Ctrl`` 替换为 ``Cmd``。


搜索类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    - Ctrl + Shift + P              Go to everything
    - Ctrl + P                      Jump into File, Symbol, Function, ...
    - Ctrl + R                      Jump to Symbol, Class, Function
    - Ctrl + ;                      Goto word in current file
    - Ctrl + G                      Jump to line by line number


选择类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    - Ctrl + D                      Select word - Repeat select others occurrences
    - Ctrl + Shift + L              MutipleLine selection and manipulate
    - Ctrl + Shift + M              In-Bracket​ selection
    - Ctrl + F                      Search
    - Ctrl + H                      Replace


编辑类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    - Ctrl + Enter                  Create new line under current line and jump to it
    - Ctrl + Shift + Enter          Create new line above current line and jump to it
    - Ctrl + Shift + Up/Down        Move selected line Up/Down
    - Ctrl + M                      Jump between bracket
    - Ctrl + J                      Join lines
    - Ctrl + N                      Create new file
    - Ctrl + Shift + N              Create new windows

    - Alt + Shift 1/2/3,...         Screen split
    - F11                           Full Screen
    - Shift + F11                   Full Screen without menu


代码类:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    - Ctrl + `                      Open Python console
    - Ctrl + B                      Build and run


高级实用技巧
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


快速选择并替换
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 方法一: 选中文本按 Alt + F3, 即可选中所有同样的文本, 然后直接修改即可。注意, 该方法不区分大小写。
2. 方法二: Ctrl + F 进入搜索框, 执行搜索后按 Alt + Enter, 进入批量编辑模式, 同时编辑所有项。


多行编辑
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

利用多行编辑给多行文本两边加上双引号, 逗号, 然后合并成一行

从::

    Apple
    Banana
    Orange

变成::

    ["Apple", "Banana", "Orange",]

1. 选中多行, Ctrl + Shift + L。
2. 按Home键切换到多行首部, 加上双引号, 再按End键切换到尾部, 加上双引号和逗号。
3. 在选中多行的状态下, 按 Ctrl + J 将多行连接成一行, 并在头尾加上方括号。


在目录下的所有文件中搜索
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Ctrl + Shift + F, 打开
2. 在Where处填入你要搜的目录, 多个目录用逗号隔开
3. 在Find处填入你要搜的关键字