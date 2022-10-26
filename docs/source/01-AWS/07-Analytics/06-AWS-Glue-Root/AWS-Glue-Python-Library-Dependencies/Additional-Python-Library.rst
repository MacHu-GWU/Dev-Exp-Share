
如何为 Glue Job 添加额外的 Python Library
==============================================================================


Ref:

- https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html

在创建 Glue Job 的时候 有两个 Parameter 跟 Python Library 有关:

- ``--additional-python-modules``: 一个 ``,`` separate 的字符串, 每个元素是 单个 Python 包的 ``.whl`` 文件, 而 **不能是一个包含了很多文件夹的 .zip 文件, 比如你把 site-packages 里的文件压缩成一个 .zip 文件 这样是错的**. 一个正确的例子是 ``s3://my-bucket/glue-library/module_a.whl,s3://my-bucket/glue-library/module_b.whl``. 该参数在运行的时候无法被显示指定的 parameter overwrite 掉.
- ``--extra-py-files``: 一个 ``,`` separate 的字符串, 每个元素是一个 ``.zip`` 文件. 里面可以是一个 ``.py`` 文件, 也可以是一个 ``module`` 的文件夹, 也可以是多个 ``module`` 的文件夹. 如果你解压出来的文件结构跟 ``site-packages`` 里面是一样的, 说明是对的. 注意解压后不能包含 ``site-packages`` 目录本身. 这个参数是可以在 Run Glue Job 的时候指定并 overwrite 掉.

在创建 Glue Dev Endpoint 的时候,

- ``ExtraPythonLibsS3Path``