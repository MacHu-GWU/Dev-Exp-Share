.. contents::

Global Setting Guide
===================================================================================================


Edit General Text Editor Setting
---------------------------------------------------------------------------------------------------
Sublime使用json文件定义所有的设置, 我们可以通过以下两种方式修改其配置:

- 1. 从菜单进入: ``Menu`` -> ``Preference`` -> ``Setting`` - ``Users``
- 2. 直接编辑配置文件: ``C:\Users\{your-username}\AppData\Roaming\Sublime Text 3\Packages\User\Preferences.sublime-settings``

My favorite setting:


.. code-block:: javascript

    {
        "theme": "Boxy Monokai.sublime-theme", // Sublime主题名称
        "color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme", // 颜色主题名称
        "font_face": "Inziu Iosevka SC", // 字体名称
        "font_size": 12, // 字体大小

        "highlight_line": true, // 是否高亮游标所在行
        "highlight_modified_tabs": true, // 是否在顶部已打开的文件栏高亮修改后但未保存的文件

        "bold_folder_labels": true, // 是否将左侧的文件浏览器目录中的文件夹加粗
        "preview_on_click": true, // 是否在单击文件时预览文件, 双击才是打开
        "remember_open_files": true, // Alt + F4 关闭sublime后, 下次打开时是否自动打开上次已打开的文件

        "fade_fold_buttons": false, // 是否自动隐藏非游标当前所在的代码折叠按钮

        "line_padding_bottom": 0, // 列前行距, 单位像素
        "line_padding_top": 0, // 列后行距, 单位像素

        "spell_check": true, // 是否打开拼写检查

        "tab_completion": false, // 是否使用tab键自动补全
        "tab_size": 4, // tab键等效的空格数
        "translate_tabs_to_spaces": false, // 自动将tab键转化为空格

        "word_wrap": true, // 是否打开自动断行
        "wrap_width": 100, // 自动断行的位置
        "rulers": // 标尺的位置, 可以有多个标尺
        [
            100,
        ],

        "draw_white_space": "all", // 显示所有的空白字符
        "indent_guide_options": // 缩进助手设置
        [
            "draw_normal", // 画出所有普通的indent
            "draw_active", // 高亮游标所激活的indent
        ],

        "ignored_packages": // 禁用的package
        [
            "RestructuredText", //
            "Vintage", // Vintage is a vi mode editing package for Sublime Text. It allows you to combine vi's command mode with Sublime Text's features, including multiple selections.
        ],
    }

- ref: http://docs.sublimetext.info/en/latest/reference/settings.html
- ref: https://www.sublimetext.com/docs/3/settings.html


Syntax Specified Settings
---------------------------------------------------------------------------------------------------
Sublime允许为每一种类型的文件配置独特的设定, 比如为Python文件的设定就会覆盖全局的设定。


Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
        "rulers": // 标尺的位置, 可以有多个标尺
        [
            80
        ],
        "tab_size": 4, // tab键等效的空格数
        "translate_tabs_to_spaces": true, // 自动将tab键转化为空格
        "word_wrap": false, // 是否打开自动断行
    }


RestructuredText
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
        "spell_check": true, // 是否检查拼写
        "tab_size": 4, // 制表符等于多少个空格
        "translate_tabs_to_spaces": true // 自动将tab键转化为空格
    }


Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
        "rulers": // 标尺的位置, 可以有多个标尺
        [
            100,
            200
        ],
        "tab_size": 4, // tab键等效的空格数
        "translate_tabs_to_spaces": true, // 自动将tab键转化为空格
        "word_wrap": true, // 是否打开自动断行
        "wrap_width": 200, // 自动断行的位置
    }


Keymap Setting
------------------------------------------------------------------------------
Keymap设置控制着键盘操作的行为。``Menu`` -> ``Preference`` -> ``Key Binding`` 可以进入自定义的键位设置。


自定义自动配对的符号
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
默认设置中Sublime只能自动配对 ``'``, ``"``, ``()``, ``{}``, ``[]`` 这些符号。而在RestructuredText和Markdown中我们也会需要对 ``*`` (加粗) 和 ````` (等宽代码) 进行自动配对。

将以下设置添加到User Keymap Setting可以实现这一点。

.. code-block:: javascript

    [
        // Auto-pair stars
        { "keys": ["*"], "command": "insert_snippet", "args": {"contents": "*$0*"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^(?:\t| |\\)|]|\\}|>|$)", "match_all": true },
                { "key": "preceding_text", "operator": "not_regex_contains", "operand": "[*a-zA-Z0-9_]$", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true }
            ]
        },
        { "keys": ["*"], "command": "insert_snippet", "args": {"contents": "*${0:$SELECTION}*"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }
            ]
        },
        { "keys": ["*"], "command": "move", "args": {"by": "characters", "forward": true}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^*", "match_all": true },
                { "key": "selector", "operator": "not_equal", "operand": "punctuation.definition.string.begin", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true },
            ]
        },
        { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Left Right.sublime-macro"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "preceding_text", "operator": "regex_contains", "operand": "*$", "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^*", "match_all": true },
                { "key": "selector", "operator": "not_equal", "operand": "punctuation.definition.string.begin", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true },
            ]
        },

        // Auto-pair `
        { "keys": ["`"], "command": "insert_snippet", "args": {"contents": "`$0`"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^(?:\t| |\\)|]|\\}|>|$)", "match_all": true },
                { "key": "preceding_text", "operator": "not_regex_contains", "operand": "[`a-zA-Z0-9_]$", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true }
            ]
        },
        { "keys": ["`"], "command": "insert_snippet", "args": {"contents": "`${0:$SELECTION}`"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }
            ]
        },
        { "keys": ["`"], "command": "move", "args": {"by": "characters", "forward": true}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^`", "match_all": true },
                { "key": "selector", "operator": "not_equal", "operand": "punctuation.definition.string.begin", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true },
            ]
        },
        { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Left Right.sublime-macro"}, "context":
            [
                { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
                { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
                { "key": "preceding_text", "operator": "regex_contains", "operand": "`$", "match_all": true },
                { "key": "following_text", "operator": "regex_contains", "operand": "^`", "match_all": true },
                { "key": "selector", "operator": "not_equal", "operand": "punctuation.definition.string.begin", "match_all": true },
                { "key": "eol_selector", "operator": "not_equal", "operand": "string.quoted.double - punctuation.definition.string.end", "match_all": true },
            ]
        },
    ]
