AWS Lambda Concurrency Strategy
==============================================================================

- Managing AWS Lambda Function Concurrency: https://aws.amazon.com/blogs/compute/managing-aws-lambda-function-concurrency/
- AWS Lambda Function Scaling: https://docs.aws.amazon.com/lambda/latest/dg/scaling.html
- Serverless Providers: A Comparative Analysis of AWS Lambda, Azure Functions & Google Cloud Functions: https://kruschecompany.com/serverless-providers-comparison/


How to Calculate the Concurrency You need
------------------------------------------------------------------------------

- 每秒钟有 100 个请求
- 每个请求平均需要 3 秒进行处理
- 那么你需要 300 个请求需要处理


Concurrency 的底层是如何实现的
------------------------------------------------------------------------------

参考资料:

- Managing Concurrency for a Lambda Function: https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html
- AWS Lambda Function Scaling: https://docs.aws.amazon.com/lambda/latest/dg/scaling.html

- 我们这里说的 Concurrency 是指的实际运行 Lambda 的 Container 的数量, 因为 Lambda 的底层是运行在大量 EC2 上的 Container.
- AWS 每个 Region 内所有的 Function 的 Concurrency 不得超过 1000. 但是这个数字可以通过打电话请求 AWS 提高上限.
- AWS 不同的 Region 有一个 Burst Concurrency Limits, 在美国本土, 亚洲, 其他地区分别是 3000, 1000, 500. 这个是你在请求一下子涌入爆发增长时的允许使用指数级快速 scale up 的上限, 过了这个上限就只能线性的平缓 scale up 了.
- 对每一个 Function, 你可以设置 **Reserved Concurrency Limit**. 这个 limit 会阻止其他 function 使用这些资源, 也会组织此 function 使用其他的 Unreserved 的资源. 这个 limit 会占用你的 Regional Concurrent Limit.
- 对每一个 Function, 你还可以设置 **Provisioned Concurrency**. 这是一种通过提前初始化 Container 而避免 Cold Start 导致的延迟波动的策略, 但是 Provisioned Concurrency
- 如果一下子就初始化 Provisioned Concurrency 所设定的机器, 但请求却没有达到这么多, 那么会造成浪费. 为了解决这个问题你可以使用 **Application Auto Scaling**, 通过定义一些 Metrics, 自动的一步一步的 Scale Up/Down. 从而达到节约资源的目的.

**在没有设置 Reserve Concurrency Limit 时**:

1. 首先在达到 Burst Concurrency Limits 之前, 请求来多少, 就自动按指数 scale up 到多少.
2. 到达 Burst Concurrency Limits 之后, Concurrency 线性增长. 如果在线性增长期间请求超过了 Concurrency 的负载, 那么那些多出来的请求则会收到 429 Throttling Error.
3. 当负载减少时, 会自动关闭 Container.

**在设置了 Provisioned Concurrency 时, 但没有 Application Auto Scaling 时, 请求并发是如何实现的**:

1. 一开始就会有 ``Provisioned Concurrency`` 这么多的机器被初始化.

**在设置了 Provisioned Concurrency 时, 而且有 Application Auto Scaling 时, 请求并发是如何实现的**:

1. 一开始只有少量的 container 被初始化, 随着请求的增加会慢慢增长.


思考题1:

如果有一个 Lambda Function 用于帮助 AWS Cognito 执行自定义用户登录请求. 平均运行时间为 2 秒. 这个用户登录请求需要跟位于 Private VPC Subnet 的 Database 进行交互. 用户的请求比较难预测, 会从 100 - 500 之间波动. 我们需要保证, 用户提交登录请求的处理时间不超过 3 秒, 尽量节约运行成本. 请问你会如何配置 Lambda Function.

答案:

1. 首先分析要解决的问题, 第一是跟 Private VPC 通信, 那么 cold start 的时间会比较长, 大约是 10-20 秒, 这是无法接受的. 另一个就是如果我们预热 Container, 那么我们需要







