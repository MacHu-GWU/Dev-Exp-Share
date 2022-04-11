.. _add-extra-python-library-to-glue-job-or-dev-endpoint:

Add Extra Python Library to Glue Job or Dev Endpoint
==============================================================================
Keywords:

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Challenge
------------------------------------------------------------------------------
Glue Dev Endpoint 自带一些常用的 Python 包, 例如 Numpy, Pandas 等. 如果你需要其他的 Python 包的话, 你不能用 Notebook 中的魔法命令 ``%pip install ...``, 因为 Glue Dev Endpoint 上面的代码是通过 PySpark Magic 发送到 Spark 集群上远程执行的. 而 ``%pip install ...`` 只能为 Notebook Instance 本身安装 Python 包.

AWS 推荐的做法是为 Glue Dev Endpoint 添加 Python 包, 本质上就是将依赖安装到 ``site-packages`` 目录下, 然后压缩成 ``site-packages.zip`` (注意, 压缩包是在 site-packages 目录内进行压缩的, 并不带 site-packages 这个目录本身), 并用 ``aws glue update-dev-endpoint`` 命令对其进行更新即可.

这里要注意几点:

- Glue 只支持 Pure Python Library, 而不支持依赖 C 的包. 例如你如果想 upgrade ``numpy``, ``pandas`` 的版本是做不到的.
- Glue Dev Endpoint 的 Glue 版本是 1.0 而 Python 的版本是 3.6, 而文档 https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue20-modules-provided 中的提到的 Glue 自带的包列表是 2.0 的. 而且有些新的包不支持 Python 3.6.
- 你如果在 Glue Job 中使用 2.0, 3.0 版本, 则对应的 Python 版本是 3.7. 也就是说你开发的时候要 build 一次 Python Library. Deploy 到 Glue Job 又要 build 一次, 还挺麻烦的.

参考资料:

- Glue Dev Endpoint 中 Glue 的版本信息: https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint.html
- Glue Dev Endpoint 中自带的 Python 库的信息: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue20-modules-provided
- 关于 Glue Dev Endpoint 无法添加依赖 C 的包的声明: https://docs.aws.amazon.com/glue/latest/dg/add-dev-endpoint.html
- Glue Release Note, Glue 版本号以及支持的 Spark, Python 版本的对应关系: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html


Build Python Library For Glue
------------------------------------------------------------------------------
前期准备工作:

1. 找到对应的 Glue 版本: 首先你需要知道你 build 的 Python Library 是给 Glue Job 用的 还是给 Glue Dev Endpoint 用的. 比如我们这里是给 Glue Dev Endpoint 用的, 那么只有一个版本就是 Glue 1.0.
2. 找到与 Glue 版本对应的 Python 版本: 根据 Release Note 对应的 Python 版本是 Python3.6
3. 给 Glue Dev Endpoint 添加 SSH Public Key, 然后 SSH 上去以后打 ``pip freeze`` 命令查看预装的 Python 包以及版本. 这里 ``glue1.0-pre-installed-python-library.txt``, ``glue2.0-pre-installed-python-library.txt`` 已经把这些工作给做好了. 这些已经有的包就不要重复安装了.

建议使用

::

    aws glue update-dev-endpoint --endpoint-name "${dev_endpoint_name}" --add-public-keys "ssh-rsa ......
    ssh glue@ec2-13-59-145-121.us-east-2.compute.amazonaws.com

该文件夹提供了一些便利的脚本, 以用于为 Glue Job 或者 Glue Dev Endpoint 配置额外的 Python Library.


aws glue update-dev-endpoint --endpoint-name "glue-etl-dev" --custom-libraries ExtraPythonLibsS3Path="s3://sandbox-userhome/aip/sanhe.hu/glue/python-library/site-packages.zip" --update-etl-libraries --profile afs_dev