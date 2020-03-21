DockerHub Docs
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
