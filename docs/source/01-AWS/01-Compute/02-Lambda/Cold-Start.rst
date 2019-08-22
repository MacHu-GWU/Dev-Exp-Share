AWS Lambda Cold Start
==============================================================================

Reference:

- Cold Starts in AWS Lambda: https://mikhail.io/serverless/coldstarts/aws/
- From 0 to 1000 Instances How Serverless Providers Scale Queue Processing: https://mikhail.io/2018/11/from-0-to-1000-instances-how-serverless-providers-scale-queue-processing/
- Everything you need to know about cold starts in AWS Lambda: https://hackernoon.com/cold-starts-in-aws-lambda-f9e3432adbf0
- Keeping Functions Warm How To Fix AWS Lambda Cold Start Issues: https://serverless.com/blog/keep-your-lambdas-warm/
- I’m afraid you’re thinking about AWS Lambda cold starts all wrong: https://theburningmonk.com/2018/01/im-afraid-youre-thinking-about-aws-lambda-cold-starts-all-wrong/

结论:

- 动态语言快, 但差距不明显, C#最慢 (有特殊原因).
- Deployment Package 越大, 速度越慢, 如果 Layer 50MB 以上, 可能要个 1-10 秒.
- Memory Size 不怎么影响 Cold Start.
- VPC Access 需要 10 - 15 秒, 这是因为 AWS 需要在 VPC 里的 Subnet 中找一个 IP 用于运行你的容器.

Cold Start 和 Concurrency 的关系: 每个 Concurrency 都要 Launch 一个 Container, 也就是说在 Scale Up 时, 每多一个 Concurrency 都必须经历 Cold Start. 也就是说你的 App 并发突然增大, 结果每个并发都会触发 Cold Start.

Concurrency 和 VPC Subnet 的关系: subnet 的 EIP 数量必须必 Concurrency 的数量要多. 比如如果你用的 xxx.xxx.xxx.xxx:24, 那么你只有 256 个IP, 也就是最多 256 个并发.