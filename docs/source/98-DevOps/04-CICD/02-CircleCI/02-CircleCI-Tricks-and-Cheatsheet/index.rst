.. _circleci-tricks-and-cheatsheet:

CircleCI Tricks and Cheatsheet
==============================================================================


Document
------------------------------------------------------------------------------



Securely Inject Secret / Sensitive Information
------------------------------------------------------------------------------

Reference:

- https://circleci.com/docs/2.0/contexts

CircleCI 提供了两种方式用于读取敏感信息.

1. 使用 Context. Context 是 Organization 级别的数据. 你可以在任何 projects 中引用 Context 中的数据. 你可以创建任意多个 Context. 同时你可以使用 Security Group 来管理哪些用户可以访问哪些 Context.
2. 使用 Environment Variable. Env Var 是 Project 级别的数据. 你只能在当前 Project 中引用这些数据.

使用 Context:

1. 打开 Jobs 菜单, 点击 Settings (或齿轮)
2. 进入 Context 菜单, 点击 Create Context 创建一个 Context 环境.
3. 将敏感信息存入 Context 中的 Environment Variables. 然后在 CI 的 Bash scripts 中用 ``${VAR_NAME}`` 引用之.

使用 Environment Variable:

1. 打开 Workflows 菜单, 点击具体的 project, 点击 Settings (或齿轮)
2. 编辑 Environment Variables 菜单. 然后在 CI 的 Bash scripts 中用 ``${VAR_NAME}`` 引用之.

还有一种方法可以实现安全引用各种敏感信息和复杂的数据结构.

具体操作很简单, 本质上是在 Context 中设定一个 AWS ACCESS KEY 和 AWS SECRET KEY, 其背后的 IAM User 被允许访问 kms, secret manager, system manager parameter store. 然后使用 secret manager 和 parameter store 保存敏感数据, 然后再 runtime 中使用 aws cli 来访问敏感数据.😆🤣p`1txcjv,./
]\=06fe
]\)P:Åxs    c.v07-=(0p;./-].
' 吗>


SSH to Job Instance to Debug
------------------------------------------------------------------------------

Reference:

- https://circleci.com/docs/2.0/ssh-access-jobs/

集成环境出了问题? CircleCI 允许你 SSH 到远程虚拟机里的 Shell 环境中进行调试.

1. 进入 job 页面, 选择右上角的 Rerun job with SSH. CircleCI 在连接你的 Github 之后, 会自动创建一个 SSH 用于连接到集成环境的虚拟机.
2. 打开界面里的 Enable SSH, 里面有一条信息是: You can now SSH into this box ..., 复制下面的 SSH 连接代码即可连接到虚拟机的根目录下.


Use Docker in Docker
------------------------------------------------------------------------------

Reference:

- https://circleci.com/docs/2.0/building-docker-images/

因为 CircleCI 的 runtime 本身是 docker, 而在 docker 中运行 docker 本身会带来一些问题. 下面是在 CircleCI 中如何使用 docker 的方法.

有时我们需要在 CI 环境中使用 docker 命令, 通常是用于自动化构建自定义的 Docker Image 的项目 (自定义 DockerFile, 在本地构建一个 Image, 然后测试该 Image, 如果测试成功, 则将其发布到 DockerHub 上). 在 CircleCI 中, 需要在 ``steps:`` 中设定 ``- setup_remote_docker`` 才能使 ``docker ..`` 命令生效. (实质上时将这些命令放到宿主机器上执行)::

    jobs:
      <job_name>:
        steps:
          - checkout
          - setup_remote_docker


Use Database Container Service for Test
------------------------------------------------------------------------------

Reference:

- https://circleci.com/docs/2.0/databases/

如果我们的测试环境需要使用 数据库之类的 docker 进行测试, 由于运行时本身是 docker, 所以无法在 docker 中运行一个 database 的 docker 然后连接之. 而且出于安全考虑 CircleCI 不允许对系统的 Port 进行修改, 所以我们无法通过下载 postgresql 的 docker image, 然后再本地开一个 port 运行.

但是 CircleCI 自带各种数据库的 image, 可以在 config.yml 文件中进行设置, 在启动 Job 时自动启动数据库服务.

如果需要 Ngnix 或其他本地服务, 可以用同样的方法实现.


Checkout Additional Private Repository
------------------------------------------------------------------------------

当你连接了 GitHub Repo 之后, CircleCI 可以从该 Repo 处 Pull 代码. 但是如果你的项目需要从其他的 Private Repo 处 Pull 代码用于构建, 你要怎么做?

方法 1:

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

方法 2:

为另外的 Repo 启用一个 CircleCI Pipeline, 然后将代码打包上传到 AWS S3, 然后在你当前的 Pipeline 中从 AWS S3 下载代码.


Reuse YAML Node or Code Snippet
------------------------------------------------------------------------------

YAML 支持定义一个 anchors 或者 alias, 然后在其他地方引用之, 以达到重复利用代码的目的.

定义的标记是 ``&``, 引用有两个标记, ``*`` 是指完全拷贝. 而 ``<<: *`` 是指继承并修改一些子节点.

简单来说就是::

    definitions:
      steps:
        - step: &build-test
            name: Build and test
            script:
              - mvn package
            artifacts:
              - target/**

    pipelines:
      branches:
        develop:
          - step: *build-test
        master:
          - step:
              <<: *build-test
              name: Testing on Master


等价于::

    definitions:
      steps:
        - step: &build-test
            name: Build and test
            script:
              - mvn package
            artifacts:
              - target/**

    pipelines:
      branches:
        develop:
          - step:
            name: Build and test
            script:
              - mvn package
            artifacts:
              - target/**
        master:
          - step:
            name: Testing on Master
            script:
              - mvn package
            artifacts:
              - target/**


Reference:

- https://confluence.atlassian.com/bitbucket/yaml-anchors-960154027.html
- https://en.wikipedia.org/wiki/YAML#Advanced_components
