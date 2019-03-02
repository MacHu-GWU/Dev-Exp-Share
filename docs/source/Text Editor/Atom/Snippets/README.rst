Atom中的Snippet功能
==============================================================================
`See tutorial here <https://atom.io/packages/snippets>`_

Atom最强大的功能之一就是自定义化度极高的Snippets功能。本身Atom就通过Package的方式为各种语言内置了许多代码块，还能允许用户自定义自己的代码块。

例如你想为Python语言设置一个代码块，具体步骤是这样子的:

1. 菜单 -> ``Atom`` -> ``Snippets``, 打开 ``snippets.cson`` 文件.
2. 自定义的 snippets 的语法是这样子的:

.. code-block:: CoffeeScript

    '.source.python':
      'from __future__ import xxx':
        'prefix': 'future'
        'body': """
          from __future__ import (
              print_function, unicode_literals, absolute_import,
              division, generators,
          )
        """

    '.source.{language scope}':
      '{snippet name}':
        'prefix': '{snippet toggle}'
        'body': '{snippet body}'


Language Scope
------------------------------------------------------------------------------
想知道各语言对应的Scope，可以进入 ``Settings`` 菜单, 然后选择 ``Package``，在 ``Installed Package`` 中搜索 ``language``，下面就会显示出对应语言的package，拖到下面（以Python为例）**Python Grama** 一栏，就可以看到 ``Scope: source.python``。


Snippet Body
------------------------------------------------------------------------------
输入了 prefix 然后按下 tab 呼出代码块之后，``$(1:Place Holder)`` 语法可以占用让用户输入的部分。默认是$1的位置，填写完毕后按下Tab跳转到$2的位置。在定义了$1之后，可以在body中其他位置用 ``$1`` 来代替整个 ``(1:Place Holder)``。

例如Python中的::

.. code-block:: CoffeeScript

    '.source.python':
      'New Class':
        'prefix': 'class'
        'body': 'class ${1:ClassName}(${2:object}):\n\t"""${3:docstring for $1.}"""\n\tdef __init__(self, ${4:arg}):\n\t\t${5:super($1, self).__init__()}\n\t\tself.arg = arg\n\t\t$0'
