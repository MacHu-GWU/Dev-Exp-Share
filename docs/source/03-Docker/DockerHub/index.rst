DockerHub
==============================================================================

DockerHub 是一个类似于 GitHub 的容器仓库管理托管平台. 你可以将你的容器发布在 DockerHub 上, 公开的容器可以被其他开发者所使用. 当然你也可以付费使用私有容器供企业使用. 相对应的 AWS 服务是 ECR. 更重要的是 DockerHub 自带 CI/CD 系统, 允许连接 GitHub, 然后自动根据 Dockerfile 进行构建.

DockerHub 是一个 repository registration service, 而 AWS ECR 则是另一个 repository registration service.

docker client 命令行工具可以将你在本地机器上构建的 image push 到 DockerHub 上.



使用 DockerHub 服务
------------------------------------------------------------------------------

**登录**

1. 首先你需要登录. 最简单的登录方式是使用 ``docker login`` 命令, 然后输入账号密码即可. 如果你需要切换 registration 服务, 那么你需要运行 ``docker logout`` 命令 然后再次输入 ``docker login``. 注意, 直接使用 ``docker logout --username foo --password bar`` 是不安全的, 因为命令行日志可能会暴漏你的密码.
2. 如果你想要避免交互式的输入账号密码, 那么建议如果你想要将密码以明文方式保存在本地机器上 (类似于 ``~/.aws/credential`` 文件的方式), 然后从文件读取, 那么你可以使用 ``cat ~/my_password.txt | docker login --username foo --password-stdin`` 命令. 由于在 Linux 机器上你可以对 密码文件 进行权限管理和保护, 设为只对某些用户可读, 所以这样做是安全的.

参考资料:

- https://docs.docker.com/engine/reference/commandline/login/

- 从 Dockerfile 构建镜像: ``docker build -t <username>/<repo-name>:<tag> <path-to-dockerfile-dir>``, 如果 Dockerfile 就在当前目录, 那么则使用 ``.`` 代替 ``<path-to-dockerfile-dir>``.
- 给构建好的本地镜像打上其他标签: ``docker tag <old-username>/<old-repo-name>:<old-my-tag> <new-username>/<new-repo-name>:<new-my-tag>
- 将你本地的镜像推送到远程仓库中: ``docker push <username>/<repo-name>:<tag>``


使用 ECR 服务
------------------------------------------------------------------------------

只要你登录了 AWS ECR 服务, 那么之后的 push, pull 等命令都和 dockerhub 一致. 关于验证, 你需要先运行 ``aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>`` 获得一个 token, 然后使用 ``docker login -u AWS`` 命令手动输入密码后登录. 之所以不使用 ``-p`` 选项是因为命令行中输入的命令都有记录, 会有暴漏的风险. 对于希望使用自动化构建来将新构建好的镜像推送到 ECR 的情况, 请参考这篇文档: https://aws.amazon.com/blogs/devops/build-a-continuous-delivery-pipeline-for-your-container-images-with-amazon-ecr-as-source/

.. list-table:: Comparison
    :widths: 10 10 10
    :header-rows: 1

    * -
      - DockerHub
      - AWS ECR
    * - Login Command
      - .. code-block:: bash

            docker login
      - .. code-block:: bash

            aws ecr get-login --region <aws-region> --no-include-email --profile <aws-profile>
            docker login -u AWS
    * - Repository
      - .. code-block:: bash

            <dockerhub-username>/<repo-name>
      - .. code-block:: bash

            <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<repo-name>
    * - Push Command
      - .. code-block:: bash

            docker push <dockerhub-username>/<repo-name>:<tag>
      - .. code-block:: bash

            docker push <aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<repo-name>:<tag>

参考资料:

- https://docs.aws.amazon.com/AmazonECR/latest/userguide/registries.html


aws ecr get-login --region us-east-1 --no-include-email --profile eq_sanhe

docker tag sanhe/cicd:awscli-python3.6.8-packer-slim 110330507156.dkr.ecr.us-east-1.amazonaws.com/aws-ls-docker:awscli-python3.6.8-packer-slim

docker push 110330507156.dkr.ecr.us-east-1.amazonaws.com/aws-ls-docker:awscli-python3.6.8-packer-slim