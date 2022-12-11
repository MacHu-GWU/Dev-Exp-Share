Typing Extensions
==============================================================================
Typing 这个模块是 Python3.5 加入的, 随时时间的推移, 越来越多的功能被加入这个标准库. 但是对于第三方包开发者, 你需要支持很多 Python 版本 (到 2023 年初, 一般的包都是要支持 Python3.7+ 的, 根据 `end of life <https://endoflife.date/python>`_) 3.7 在 2023 年 1 月停止支持. 如果你用到了高版本的 Typing 的功能, 那么你在低版本的时候如何保持兼容呢? `typing-extensions <https://pypi.org/project/typing-extensions/>`_ 这个库就允许你在低版本 (也至少要有 3.7+) 使用高版本的功能. 你只要把你的 ``import typing as T`` 替换成 ``import typing_extensions as T`` 即可.

而对于 Python2.7, 3.4 之类的版本, 你如果想要用 typing 的话, 就需要用到 ``typing <https://pypi.org/project/typing/>`_ 这个 backport 用来向前兼容的包了.
