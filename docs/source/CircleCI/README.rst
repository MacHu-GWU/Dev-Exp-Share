.. _circleci-reference:

CircleCI Reference
==============================================================================

docs:

- config.yml reference: https://circleci.com/docs/2.0/configuration-reference
- list of built-in docker images: https://circleci.com/docs/2.0/circleci-images


SSH to Job Instance to debug
------------------------------------------------------------------------------

- reference: https://circleci.com/docs/2.0/ssh-access-jobs/

集成环境出了问题? CircleCI 允许你 SSH 到远程虚拟机里的 Shell 环境中进行调试.

1. 进入 job 页面, 选择右上角的 Rerun job with SSH. CircleCI 在连接你的 Github 之后, 会自动创建一个 SSH 用于连接到集成环境的虚拟机.
2. 打开界面里的 Enable SSH, 里面有一条信息是: You can now SSH into this box ..., 复制下面的 SSH 连接代码即可连接到虚拟机的根目录下.


Securely Include Secret Information
------------------------------------------------------------------------------

- reference: https://circleci.com/docs/2.0/contexts

1. 打开 Jobs 菜单, 点击 Settings (或齿轮)
2. 进入 Context 菜单, 点击 Create Context 创建一个 Context 环境.
3. 将敏感信息存入 Context 中的 Environment Variables. 然后在 CI 的 Bash scripts 中用 ``${VAR_NAME}`` 引用之.

Context (上下文) 为你所有的 jobs 提供了一套上下文. 建议使用 环境变量 储存敏感信息.


Use Database Container Service for Test
------------------------------------------------------------------------------

- reference: https://circleci.com/docs/2.0/databases/

出于安全考虑 CircleCI 不允许对系统的 Port 进行修改, 所以我们无法通过下载 postgresql 的 docker image, 然后再本地开一个 port 运行.
但是 CircleCI 自带各种数据库的 image, 可以在 config.yml 文件中进行设置, 在启动 Job 时自动启动数据库服务.


Use Docker Command
------------------------------------------------------------------------------

- reference: https://circleci.com/docs/2.0/building-docker-images/

有时我们需要在 CI 环境中使用 docker 命令, 通常是用于自动化构建自定义的 Docker Image 的项目 (自定义 DockerFile, 在本地构建一个 Image, 然后测试该 Image, 如果测试成功, 则将其发布到 DockerHub 上). 在 CircleCI 中, 需要在 ``steps:`` 中设定 ``- setup_remote_docker`` 才能使 ``docker ..`` 命令生效::

    jobs:
      <job_name>:
        steps:
          - checkout
          - setup_remote_docker


Checkout Additional Private Repository
------------------------------------------------------------------------------

Reference: https://circleci.com/docs/2.0/gh-bb-integration/#enable-your-project-to-check-out-additional-private-repositories

