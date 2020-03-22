AWS Elastic Container Service (ECS) Docs
==============================================================================

ECS 是亚马逊用来部署容器应用的服务. 基本功能有:

- Run containers at scale
- Flexible container placement
- Integrated and extensible

该服务的对标产品是 Kubernetes.

比如 K8s 的 Pod 对应 ECS Task Definition.


Launch Type
------------------------------------------------------------------------------

- Fargate Launch Type: Fargate 免除了管理你的 EC2 Cluster 的麻烦, 而是在 AWS 的一个超大的虚拟机池子里运行你的容器. 你只需要自定义你的 Container, 然后 AWS 帮你启动需要的容器即可.
- EC2 Launch Type: 允许你在你所管理的 EC2 Cluster 上运行 Container.

Reference:

- Amazon ECS Launch Types: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html


