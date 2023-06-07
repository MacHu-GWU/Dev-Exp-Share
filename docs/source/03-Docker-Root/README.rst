Docker Root
==============================================================================
本文档说的是使用 Docker 进行容器镜像的开发, 运行, 部署相关的我个人的学习心得. Docker 是容器开发的工具的一种, 也是最为流行的一种, 但它不是容器技术本身. 本文还是着眼于使用容器技术解决生产环境中的问题, 而不是研究 Docker 工具本身. 当然顺带的会介绍很多 Docker 工具的使用心得.


What is "Docker"?
------------------------------------------------------------------------------
Docker 这个词有在软件工程领域有多个含义. 首先 Docker 是一家公司, 它有一个同名的产品 Docker, 它是一个容器管理工具和引擎. 容器这个词是 container, 一般我们用容器来跑应用程序也是在 container 中跑. 而容器的也叫做 container image. 容器的技术比 Docker 历史要长 10 多年, 而一般只有大公司内有自己的容器工具和技术. 而由于早期 Docker 工具的流行使得它容器技术的代名词, 在因为 Docker 工具才接触容器技术的人来说, Docker 就是 container, Docker image 就是 container image, 所以我们凡是说到 run docker 就是指的运行容器, 凡是说到 docker image 就是说的容器镜像.


Docker 学习资料
------------------------------------------------------------------------------
- Docker 从入门到实践: https://yeasy.gitbooks.io/docker_practice/
- Docker Command Line Reference: https://docs.docker.com/engine/reference/commandline/container/
- Docker Swarm (不推荐学, K8S 要更流行): https://docs.docker.com/engine/swarm/
- Docker Compose (不推荐学, K8S 要更流行): https://docs.docker.com/compose/


目录
------------------------------------------------------------------------------
.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
