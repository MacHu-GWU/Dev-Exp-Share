.. contents::

Global Setting Guide
===================================================================================================


Edit General Text Editor Setting
---------------------------------------------------------------------------------------------------
Sublime使用json文件定义所有的设置, 我们可以通过以下两种方式修改其配置:

- 1. 从菜单进入: Menu -> Preference -> Setting - Users
- 2. 直接编辑配置文件: C:\Users\your-username\AppData\Roaming\Sublime Text 3\Packages\User\Preferences.sublime-settings

My favorite setting::

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