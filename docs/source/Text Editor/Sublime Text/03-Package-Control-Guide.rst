.. contents::

Package Control Guide
==============================================================================


Package Control (包管理)
------------------------------------------------------------------------------

安装好Sublime之后第一件事就是安装Sublime的包管理软件 ``Package Control``。 安装了Package Control之后:

- 安装扩展包: Ctrl + Shift + P -> install package -> package name
- 列出已安装扩展包: Ctrl + Shift + P -> list packages -> package name
- 卸载扩展包: Ctrl + Shift + P -> remove package -> package name

Homepage: https://packagecontrol.io/installation



My Favorite Packages
------------------------------------------------------------------------------
下面列出了个人常用的插件。


General Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Side​Bar​Enhancements (侧边栏增强, 将你的侧边栏变成文件浏览器)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SideBarEnhancements gives you more option in your project explorer.

Features:

1. Copy the absolute file path in clipboard, right click -> Copy as Text -> Path
2. Copy the Unix style base path in clipboard, right click -> Copy path

Homepage: https://packagecontrol.io/packages/SideBarEnhancements


Boxy Theme (Sublime Text主题, 个人最喜欢的主题)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The most hackable theme for Sublime Text 3

Homepage: https://packagecontrol.io/packages/Boxy%20Theme

如果你有兴趣安装其他主题, 可以参考这一博文: https://scotch.io/bar-talk/best-sublime-text-3-themes-of-2015-and-2016


FileDiffs (文件改动比较)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Shows diffs between the current file, or selection(s) in the current file, and clipboard, another file, or unsaved changes.

Usage:

- Compare with Clipboard: Right click -> Diff with Clipboard

Hompage: https://packagecontrol.io/packages/FileDiffs


Bracket​Highlighter (括号高亮)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Bracket and tag highlighter for Sublime Text.

Homepage: https://packagecontrol.io/packages/BracketHighlighter


Trailing​Spaces (一键删除所有代码最后的无用空格)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Highlight trailing spaces and delete them in a flash.

Usage:

Homepage: https://packagecontrol.io/packages/TrailingSpaces


Markup Editing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Omni​Markup​Previewer (标记语言预览和Html输出支持)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Live previewer/exporter for markup files (markdown, rst, creole, textile...).

Usage:

- preview in browser: Ctrl + Alt + O
- export html: Right click -> Export Markup as HTML

Homepage: https://packagecontrol.io/packages/OmniMarkupPreviewer


Restructured​Text Improved(RST语法高亮)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Improved Syntax Highlighting for RestructuredText.

Homepage: https://packagecontrol.io/packages/RestructuredText%20Improved


Markdown​Editing (Markdown语法高亮)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Powerful Markdown package for Sublime Text with better syntax understanding and good color schemes.

Homepage: https://packagecontrol.io/packages/MarkdownEditing

修改Theme::

    // 在 Package Setting -> Markdown Editing -> Markdown GFM Setting User 中
    // 给 Markdown.sublime-settings 设置文件加入这样的代码
    {
        "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Dark.tmTheme",
    }


JsonComma (自动在 Json 中补全和删除不必要的逗号)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Homepage: https://github.com/math2001/JSONComma

保存时自动检查和更正, 在全局 Package Setting 中设置 jsoncomma_on_save 为 True 即可::

    {"jsoncomma_on_save": true}


Pretty JSON (快捷键将 Json 格式化)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Homepage: https://packagecontrol.io/packages/Pretty%20JSON

快捷键:

- Windows: ctrl+alt+j
- OS X: cmd+ctrl+j
- Linux: ctrl+alt+j


Json Key Value (让 Key Value 的颜色分开)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Homepage: https://packagecontrol.io/packages/JSON%20Key-Value


Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Batch (Windows), Bash (MacOS), Shell Script (Linux)


Bash Build System
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
允许在Sublime中运行Bash。安装: https://packagecontrol.io/packages/Bash%20Build%20System 。


Python Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Anaconda (Python IDE支持)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Anaconda turns your Sublime Text 3 in a full featured Python development IDE including autocompletion, code linting, IDE features, autopep8 formating, McCabe complexity checker and Vagrant for Sublime Text 3 using Jedi, PyFlakes, pep8, PyLint, pep257 and McCabe that will never freeze your Sublime Text 3

Features:

1. Auto Complete
2. Pep Error check
3. Go To Definition, 选中方法, 函数或类, Ctrl+Alt+G到定义处
4. Find Usage, 选中方法, 函数或类, Ctrl+Alt+F找到所有用到该函数的地方
5. Show Documentation, 选中方法, 函数或类, Ctrl+Alt+D显示文档字符串

Edit setting: Preference -> Package Setting -> Anaconda -> Setting-User

My favorite setting::

    {
        "pep8": false, // pep8标准要求所有的缩进要么全是空格，要么全是tab，不允许混用。我们不需要这个。
        "pyflakes_explicit_ignore":
        [
            //"Redefined",
            //"UnusedImport",
            //"UndefinedName",
            //"UndefinedLocal",
            //"UnusedVariable,",
            //"UndefinedExport",
            //"DuplicateArgument",
            //"RedefinedWhileUnused",
        ],
    }

Homepage: https://packagecontrol.io/packages/Anaconda


Python PEP8 Autoformat (按照PEP8 Python风格标准格式化代码)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python PEP8 Autoformat is a Sublime Text (2|3) plugin to interactively reformat Python source code according to PEP8 (Style Guide for Python Code).

Usage: ``Ctrl + Shift + R`` for (Windows/MacOS/Linux)

Homepage: https://packagecontrol.io/packages/Python%20PEP8%20Autoformat



Web Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


HTML-CSS-JS Prettify (HTML代码自动排版)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

HTML, CSS, JavaScript and JSON code formatter for Sublime Text 2 and 3 via node.js

Usage: Right click -> HTML/CSS/JS Prettify

Homepage: https://packagecontrol.io/packages/HTML-CSS-JS%20Prettify 