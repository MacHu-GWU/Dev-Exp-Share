.. _python-awesome-lib-cookiecutter:

``cookiecutter``
==============================================================================
Keywords: Cookiecutter, Template, Project, Git Repo.


Summary
------------------------------------------------------------------------------
`cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ 是一个开源 Python 项目. 可以从项目模板中生成项目. 这个项目模板本质上是一堆文件和文件夹. 特殊的是这些文件的名字以及内容都是用 `jinja2 <https://jinja.palletsprojects.com/en/3.1.x/>`_ 模版语言写成的. 这就使得你只要填写一些参数, 就可以生成一整个目录.


Templaterize
------------------------------------------------------------------------------
既然我们可以从模板生成项目, 那我们能不能从项目生成模板呢? 答案是可行的. 我们就自己实现了一个工具.

.. literalinclude:: ./templaterize.py
   :language: python




