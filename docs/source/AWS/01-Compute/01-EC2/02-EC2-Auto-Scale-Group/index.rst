Auto Scale Group (ASG)
==============================================================================

简单来说 ASG 就是一个自动启动和关闭 EC2 的管理器, 设定一个 最少, 最多的 EC2 台数, 然后 CPU 利用率高了就启动 EC2, 利用率低了就关闭 EC2.

Concept:

- Launch Template: Metadata of EC2, 决定了自动启动的 EC2 机器的详细配置, 比如用哪个 Image, 多达的 CPU 和内存.
- Launch Configuration:

- min: 最少多少台
- desired: 最开始的时候启动多少台
- max: 最多多少台

- Scale-out: 增加机器
- Scale-in: 减少机器

Reference:

- What Is Amazon EC2 Auto Scaling: https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html


Scaling Your Group
------------------------------------------------------------------------------

- Manual Scaling: 手动指定增加/减少多少台 EC2
- Scheduled Scaling: 预定时的任务, 常用于可预测的高峰, 例如 Black Friday
- Dynamic Scaling: 简单来说就是设定一个 最小 和 最大 的 EC2 数量, 用 CloudWatch 检测 EC2 的 Metrics, 比如一旦 CPU 占用率达到 90%, 则增加一台机器. 而 CPU 低于 10%, 则关闭一台.
- Scaling Cooldowns: 简单来说就是在成功的进行一次 Scale 之后, 多久之内不进行 Scale. 常用于 Dynamic Scaling 非常频繁的增加和减少你的机器的情况.



Termination Policy
------------------------------------------------------------------------------

Controlling Which Auto Scaling Instances Terminate During Scale In:

- Default Termination Policy: 哪个 AZ 上 EC2 最多, 就在那个 AZ 上关闭一个. apply to most of case
- Customizing the Termination Policy
- Instance Protection

Load Balancer Scale-in (减少机器) Scale-out (增加机器) 的具体流程: https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-termination.html

- Controlling Which Auto Scaling Instances Terminate During Scale In: https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-termination.html
- Amazon EC2 Auto Scaling Lifecycle Hooks: https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html