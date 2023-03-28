Python moto
==============================================================================

Summary
------------------------------------------------------------------------------
moto 是 mock boto 的意思, 是一个 Python 包, 用来模拟 AWS boto3 API 的行为用于测试.

- Moto official Doc, 官方文档: http://docs.getmoto.org/en/latest/docs/getting_started.html
- Moto Usage, 使用 mock 的语法: http://docs.getmoto.org/en/latest/docs/getting_started.html#moto-usage
- Implemented services, 已经实现并支持的 AWS 服务, 以及每个服务下所支持的 API: http://docs.getmoto.org/en/latest/docs/services/index.html

pip install 'moto[ec2,s3,all]'
pip install 'moto[all]'