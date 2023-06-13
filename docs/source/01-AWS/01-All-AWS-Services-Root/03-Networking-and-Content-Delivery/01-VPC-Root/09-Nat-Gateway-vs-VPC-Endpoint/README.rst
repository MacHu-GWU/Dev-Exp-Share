.. _aws-nat-gateway-vs-vpc-endpoint:

Nat Gateway vs VPC Endpoint
==============================================================================
Keywords: Nat Gateway, VPC Endpoint, Private Link

为了让你位于私网内的资源能访问 AWS Service API (Private Subnet 内默认无法访问公网), AWS 提供了 Nat Gateway 和 VPC Endpoint 两种解决方案. 其中 Nat Gateway 是一个高可用的专用设备, 用来代理私网内的资源对外部的请求, 但隔离外部对私网内的请求. 而 VPC Endpoint 是一个位于你 VPC 内的专有的 AWS Service Endpoint, 你从 VPC 内发起的 API 请求会直连到这个 Endpoint, 而这个 Endpoint 和最终的 API 请求之间也是内部直连, 所以你的流量从头至尾都没有离开过私网, 也就不存在什么中间人劫持的问题.

这两种方法是有本质区别的. Nat 解决的是访问公网的问题, 相当于把你的 Private Subnet 变成了只能出不能进的公网, 适用性更广, 所以价格也更贵. 但这种情况下你对 AWS Service API 请求的流量还是会经过公网. 而 VPC Endpoint 只解决了访问 AWS Service API 的问题, 你的流量从头至尾都没有离开过私网, 适用性更窄, 所以价格也更便宜, 但在这一特定场景下其实更加安全.

以上是从需求角度来比较, 下面我们来对比一下两者的价格:

- NAT Gateway Hourly Charge: NAT Gateway is charged on an hourly basis. For this region, the rate is $0.045 per hour. 固定费用大约是 $32/月
- NAT Gateway Data Processing Charge: 1 GB data went through the NAT gateway. The Data Processing charge will result in a charge of $0.045.
- Pricing per VPC endpoint per AZ ($/hour) = $0.01. 固定费用是 $7.2/月
- Data Processed per month in an AWS Region	vs Pricing per GB of Data Processed ($)
    - First 1 PB = $0.01 / GB
    - Next 4 PB	= $0.006 / GB
    - Anything over 5 PB = $0.004 /GB

在企业应用中, 固定费用只是毛毛雨而流量费用才是大头, 可以看出 VPC Endpoint 的价格大约是 Nat 的 1/4, 所以你的私网资源如果只是要调用 AWS Service API, 那么还是用 VPC Endpoint 划算的多.

Reference:

- `Nat Gateway Pricing <https://aws.amazon.com/vpc/pricing/>`_
- `VPC Endpoint Pricing <https://aws.amazon.com/privatelink/pricing/>`_
- :ref:`aws-vpc-endpoint`
- :ref:`aws-vpc-nat-devices`
