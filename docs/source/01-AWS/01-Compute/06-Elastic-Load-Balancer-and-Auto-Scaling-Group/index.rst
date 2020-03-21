AWS Elastic Load Balancer and Auto Scaling Group (ELB, ASG) Docs
==============================================================================

简单来说 ELB 就是一个 ``host:port/path`` 到多个具体的 EC2 的 ``host:port`` 的映射.

Concepts:

- Listener:
- Rules:
- Health Check:
- Target and Target Group.

Load Balancer Types:

- Application Load Balancer: HTTP/HTTPS, 比如 /picture 则送到 图像服务器, /request 则送到 App 服务器
- Network Load Balancer: TCP/IP, 比如 :80 则送到 图像服务器, :8080 则送到 视频服务器
- Classic Balancer: TCP/SSL or HTTP/HTTPS, Classic Load Balancers currently require a fixed relationship between the load balancer port and the container instance port.

Reference:

- Load Balancer Types: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-types.html