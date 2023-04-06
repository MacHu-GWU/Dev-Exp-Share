Use AWS Lambda for Web Crawler
==============================================================================

在生产环境中的爬虫通常是分布式的. 无论是通用的搜索引擎爬虫, 还是专用的靶向爬虫.


Lambda Function Public IP Address
------------------------------------------------------------------------------

使用 Lambda Function 作为爬虫的运算环境时, 跟单机爬虫一样, 同样会有由于单个 IP 地址快速多次的访问而导致被 BAN 的情况. 所以我们来研究一下, AWS Lambda 的公网 IP 地址到底和什么有关.

不适用 VPC 的情况:

- 短期内多次触发单个 Lambda Function 时, IP 地址不会变化. 长期不使用该 Function, 容器会被摧毁, 再次使用时容器可能会被部署到其他的网络中, 导致会被分配新的 IP 地址.
- 如果高并发能够触发 AWS 创建多个 Runtime 自动 scale out 的情况, 不同的 Runtime 的 IP 地址不同 (待验证)

使用 VPC 的情况:

- 在使用 VPC 时, Lambda 只能被部署到 Private Subnet 上 (分配了 NAT gateway 的就是 Private Subnet). 而如果没有分配 EIP, 则永远会被分配同样的 IP
- 如果没有分配 EIP, 则公网 IP 的行为跟无 VPC 时相同.


测试代码:

.. code-block:: python

    import urllib.request

    url = "http://checkip.amazonaws.com/"

    def lambda_handler(event, context):
        with urllib.request.urlopen(url) as response:
            my_ip = response.read().decode("utf-8").strip()
        return {
            "statusCode": 200,
            "body": my_ip
        }

