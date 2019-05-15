.. _circleci-reference:

CircleCI Reference
==============================================================================

.. contents::

docs:

- config.yml reference: https://circleci.com/docs/2.0/configuration-reference
- list of built-in docker images: https://circleci.com/docs/2.0/circleci-images

CircleCI 免费账户支持私有仓库的测试. 免费账户的唯一缺点就是一次同时只能并行运行一个测试.


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

1. 另外创建一个 Machine User GitHub 账号, 名字最好是用你的主 GitHub 账号 或是 Organization 账号加上 ``Machine`` 后缀. 比如我的是 ``MacHu-GWU-Machine``.
2. 在 Machine User Account 里创建一个 Personal Access Token, 并给予 Repo 的全部权限. (Account Settings -> Developer Settings -> Personal Access Token)
3. 在你的 additional private repo 里, 将 Machine User 账户添加为 Collaborator.
4. 然后再你的主 Private Repo 的 CICD 中, 使用 ``git clone "https://${PERSONAL_ACCESS_TOKEN}@github.com/${GITHUB_ACCOUNT}/${REPO}``, 即可将其他的私有仓库 Checkout 了.
5. 注意不要将这个 Personal Access Token Check in 到你的代码仓库中, 而要用安全的方法在你的 CICD 系统中引用它. 比如 CircleCI 提供了 Context, 可以将这些密码信息放入环境变量.

这样的好处是: 即使这个 Token 泄露, 也只会影响到添加了 Collaborator 的 Private 仓库.

详细分析请参考 :ref:`compare-solution-for-checkout-additional-repo-in-cicd` 一文.

Reference:

- Machine User: https://developer.github.com/v3/guides/managing-deploy-keys/#machine-users
- Enable Your Project to Check Out Additional Private Repositories: https://circleci.com/docs/2.0/gh-bb-integration/#enable-your-project-to-check-out-additional-private-repositories

