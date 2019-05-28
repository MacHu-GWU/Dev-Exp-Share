Route 53
==============================================================================

**Route 53 是干什么的**:

1. 注册域名.
2. 将通往你域名的流量, 正确地 Route 到你位于 AWS 上的 Resource, 例如 EC2, Load Blancer.
3. 检查你的 AWS 资源 的健康度. 隔一段时间 Ping 一次, 如果 Ping 不通, 则写入 CloudWatch, 并触发 SNS 通知.

帮助你理解 CNAME


Type of Record Set:

- IPv4 Address
- CNAME



Route 53 能将流量导向哪些 AWS 服务
------------------------------------------------------------------------------

**Logging, Monitoring, and Tagging**:

- AWS CloudTrail
- Amazon CloudWatch
- Tag Editor

**Routing Traffic to Other AWS Resources**:

- Amazon API Gateway
- Amazon CloudFront
- EC2
- Elastic Beanstalk
- Elastic Load Balancer
- RDS
- S3
- VPC
- Workmail

Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/integration-with-other-services.html


用 Route 53 将通往你的域名的流量导向各种 AWS Resource 该怎么做
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-aws-resources.html

- API Gateway:
- CloudFront Web Distribution:
- EC2 Instance
- AWS Elastic Beanstalk Environment:
- ELB Load Balancer:
- AWS RDS Database Instance:
- S3 Bucket:
- VPC Interface Endpoint:
- Amazon Workmail:


你有一个 S3 Bucket 开启了 Static Website Hosting, http://example-bucket.com.s3-website-us-east-2.amazonaws.com, 你想将你的域名 www.example-bucket.com 连接上你的 Static Website.

IPv4 Address with Alias

你有 4 个 EC2, 被放在了 Load Balancer 背后. 你想将你通往你域名 www.example-web-application.com 的流量导向 Load Balancer.

IPv4 Address with Alias

你有一个 RDS, endpoint 是 example-a1b2c3d4xyz.us-west-1.rds.amazonaws.com. 你用 Route53 注册了一个域名.

CNAME without Alias

你有一个公司的域名 www.example.com, 想要用 Route 53 作为 DNS provider, 并将其导向到 CDN 上.

Create an Alias record which point to CloudFront Distribution.


Troubleshoot Server Not Found error
------------------------------------------------------------------------------

- You didn't create a record for the domain or subdomain name
- You created a record but specified the wrong value
- The resource that you're routing traffic to is unavailable


Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/troubleshooting-server-not-found.html


Routing Policy
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html

- Simple routing policy – Use for a single resource that performs a given function for your domain, for example, a web server that serves content for the example.com website. 1 对 1 路由
- Failover routing policy – Use when you want to configure active-passive failover. 如果第一个 Resource 不 Healthy, 则换下一个.
- Geolocation routing policy – Use when you want to route traffic based on the location of your users. 你预先设定好, 哪个区域的用户被路由到哪里
- Geoproximity routing policy – Use when you want to route traffic based on the location of your resources and, optionally, shift traffic from resources in one location to resources in another. 根据用户的位置, 自动选择路由到最近的 (或其他自定义规则) Resource
- Latency routing policy – Use when you have resources in multiple AWS Regions and you want to route traffic to the region that provides the best latency. 当你的 App Host 在多个 Region 上时, 选择延迟最小的.
- Multivalue answer routing policy – Use when you want Route 53 to respond to DNS queries with up to eight healthy records selected at random. 同时返回多个可路由的目的地.
- Weighted routing policy – Use to route traffic to multiple resources in proportions that you specify. 加权路由, 给每个目的地加一个 Weight, 按概率取.


Health Check
------------------------------------------------------------------------------

Route 53 的 Health Check 能检查哪些指标?

- Health checks that monitor an endpoint
- Health checks that monitor other health checks (calculated health checks)
- Health checks that monitor CloudWatch alarms

Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-types.html


Monitor Health Check
------------------------------------------------------------------------------

- To view the status of a health check on **route 53 console**
- To **receive an Amazon SNS notification** when a health check status is unhealthy (console)
- To view **CloudWatch alarm status** and edit alarms for Amazon Route 53 (console)
- To view **Route 53 metrics on the CloudWatch console**

Reference: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/monitoring-health-checks.html