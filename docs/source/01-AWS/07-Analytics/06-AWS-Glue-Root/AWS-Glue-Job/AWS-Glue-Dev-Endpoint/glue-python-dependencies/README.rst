.. _add-extra-python-library-to-glue-job-or-dev-endpoint:

Add Extra Python Library to Glue Job or Dev Endpoint
==============================================================================
该文件夹提供了一些便利的脚本, 以用于为 Glue Job 或者 Glue Dev Endpoint 配置额外的 Python Library.

这里要注意几点:

- Glue 只支持 Pure Python Library, 而不支持依赖 C 的包.
- Glue Dev Endpoint 的 Glue 版本是 1.0 而 Python 的版本是 3.6, 而文档 https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue20-modules-provided 中的提到的 Glue 自带的包列表是 2.0 的. 而且有些新的包不支持 Python 3.6.

参考资料:

- Glue Dev Endpoint 中 Glue 的版本信息: https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint.html
- Glue Dev Endpoint 中自带的 Python 库的信息: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#glue20-modules-provided
- 关于 Glue Dev Endpoint 无法添加依赖 C 的包的声明: https://docs.aws.amazon.com/glue/latest/dg/add-dev-endpoint.html
- Glue Release Note, Glue 版本号以及支持的 Spark, Python 版本的对应关系: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html


说明
------------------------------------------------------------------------------

1. 找到对应的 Glue 版本: 首先你需要知道你 build 的 Python Library 是给 Glue Job 用的 还是给 Glue Dev Endpoint 用的. 比如我们这里是给 Glue Dev Endpoint 用的, 那么只有一个版本就是 Glue 1.0.
2. 找到与 Glue 版本对应的 Python 版本: 根据 Release Note 对应的 Python 版本是 Python3.6
3. 给 Glue Dev Endpoint 添加 SSH Public Key, 然后 SSH 上去以后打 ``pip freeze`` 命令查看预装的 Python 包以及版本. 这里 ``glue1.0-pre-installed-python-library.txt``, ``glue2.0-pre-installed-python-library.txt`` 已经把这些工作给做好了.

::

    aws glue update-dev-endpoint --endpoint-name "${dev_endpoint_name}" --add-public-keys "ssh-rsa ......
    ssh glue@ec2-13-59-145-121.us-east-2.compute.amazonaws.com