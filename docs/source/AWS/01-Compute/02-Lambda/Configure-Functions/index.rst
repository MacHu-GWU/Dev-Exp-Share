Configure Functions
==============================================================================

Reference: https://docs.aws.amazon.com/lambda/latest/dg/lambda-configuration.html


Manage Concurrency
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html

- Account Level Concurrent Execution Limit (ALCEL): 1000 at same time by region
- Function Level Concurrent Execution Limit (FLCEL): 函数级别的限制是 Lambda 的一项功能, 默认是关闭的. 要注意的是, 函数级别的限制一旦设置, 会减少全局的 账号级别的限制. 例如默认的的 ALCEL 是 1000, 你给一个函数预留了 100, 那么 ALCEL 就只剩下 900 了.


**位于 VPC 内的 Lambda 在并行时的注意事项**:

Concurrent executions * (Memory in GB / 3 GB)

举例, 你的 Lambda 函数需要 1G 内存, 最高峰时需要同时运行 100 个函数. 那么需要的 ENI, 也就是 IP 的数量为: ``100 * 1 / 3 ~= 33``. 由于 10.0.0.1/26 能提供 2 ** (32 - 26) = 64 个 IP, 减掉 5 个 AWS 预留的, 也就是有 59 个 IP 可用于满足在 VPC 内同时运行个 100 个 需要 1GB 内存的 Lambda 函数.

概念:

- elastic network interfaces (ENI)

Throttling Behavior:

当并行的 Lambda 函数超过限制, 则该请求不会执行 Lambda 函数.