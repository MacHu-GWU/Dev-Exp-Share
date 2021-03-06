.. contents::

Alfred
==============================================================================
Reference:

- `Alfred官网 <https://www.alfredapp.com/>`_
- `从零开始学习 Alfred：基础功能及设置 <https://sspai.com/post/32979>`_
- `OS X 效率启动器 Alfred 详解与使用技巧 <https://sspai.com/post/27900>`_

Alfred是MacOS上的一款快速启动的App，相当于Spotlight的加强版。

个人建议使用 ``双击 Cmd`` 呼出Alfred。

默认可以搜索app, system settings, user folder。


文件打开，查找 (Search File, Folder)
------------------------------------------------------------------------------
``open/find + query``，其中query支持wildcard。比如: ``R*e.rst`` -> ``Readme.rst``。

open用于打开，find用于查询。


查找 浏览器 收藏夹 (Search Web Browser Bookmarks)
------------------------------------------------------------------------------

Alfred Preferences -> Features -> Web Bookmarks


搜索 剪贴板 记录 (Search Clipboard History)
------------------------------------------------------------------------------

Alfred Preferences -> Features -> Clipboard


查找通讯录 (Search Contact)
------------------------------------------------------------------------------
直接输入名字查找。例如：David John。


英文字典 (Dictionary)
------------------------------------------------------------------------------
``define/spell {query}`` 查询单词，例如 ``define hello``。

define用于查意义，spell用于模糊拼写。


同步 Alfred 的设置 (Sync Alfred Preference)
------------------------------------------------------------------------------

Alfred Preferences -> Advances -> Syncing: Set Preference folder
