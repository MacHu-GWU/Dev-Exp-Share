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