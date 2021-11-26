- Amazon VPC Endpoints for Amazon S3: https://docs.aws.amazon.com/glue/latest/dg/vpc-endpoints-s3.html
- VPC endpoints: https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html

VPC Endpoint 是什么, 有什么用?

首先 VPC 是亚马逊的最重要的虚拟网络服务, 能让用户把虚拟机部署到私有网络上, 让虚拟机之间的通信不离开 VPC 的网络. 如果当用户从 VPC 内部发起 AWS API 的请求, 默认情况下跟你在家里的机器上发起请求是一样的, 会找到 AWS Service Endpoint 的 DNS 名字, com.amazonaws.us-east-1.s3, 通过 Internet Gateway 或是 Nat Gateway 向公网发送请求. 有的公司不希望这些请求中的数据通过公网传输. VPC Endpoint 能为 VPC 与 AWS Service Endpoint 之间建立一个私有链接, 使得请求不会离开 AWS 数据中心的私网, 从而进一步保证安全.

VPC Endpoint 的分类

1. Interface Endpoints: 具体实现技术叫做 Private Link, 他是通过把一个 Elastic Network Interface, 类似 Internet Gateway 或是 Nat Gateway, 是一个具体的硬件, 被放置在 Subnet 中, 并给予一个具体的 DNS Name 作为你想要连接的 Service Endpoint 的 Alias, 例如 vpc-1234.kinesis.us-east-1.vpce.amazonaws.com . 这个 ENI 和 Service Endpoint 之间的连接是不走公网的. 但是, 你的 API 中的请求就需要指定为这个新的 Endpoint. 而如果不指定则请求还是会走公网, 所以会有一些麻烦. 可幸的是, AWS 提供了一个选项叫做 private DNS for endpoint. 如果打开, 只要你在 VPC 内, 即使你指定的是原有默认走公网的 Endpoint, 请求也会走 ENI. 前提是你 VPC 的设置中需要打开 ``true:enableDnsHostnames`` and ``enableDnsSupport`` 这两个选项. Interface Endpoint 主要为 S3 和 Dynamodb 以外的服务提供直连. Interface Endpoint 要计费
2. Gateway Endpoint: 具体实现方式是将一个虚拟的 Gateway 放在 VPC 的边缘. Gateway 和 S3 之间的连接是走 AWS 内网的 (Interface Endpoint 是放在 Subnet 中, 而且是个实际的硬件, 所以要收费). 然后在 Route Table 中定义把请求路由到 Gateway 即可. 麻烦的是, 你需要配置 RouteTable. 好处是 Gateway Endpoint 不收费. Gateway Endpoint 只为 S3 DynamoDB 服务.
3. Gateway Load Balancer: 也是一个 ENI, 和 Interface 类似, 为特定的几个服务所使用.
