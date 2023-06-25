Amazon MWAA Quick Start
==============================================================================



创建 MWAA Environment
------------------------------------------------------------------------------
首先我们要创建一个 Airflow 的集群环境用来开发和测试. MWAA 作为一个全托管服务, 你无需任何运维知识, 只要点几下鼠标即可创建一个生产可用的 Airflow 集群. 下面我们简单说一下步骤:

1. 进入 `MWAA AWS Console <https://us-east-1.console.aws.amazon.com/mwaa/home?region=us-east-1#home>`_, 点击 "Create Environment".
2. 然后你必须要选择一个 S3 bucket 用来储存 Dag 的源码, 插件等文件. 这个 S3 bucket 必须要开启了 Versioning, 因为每个 Airflow 上的文件都需要允许被回滚的. 我建议专门创建一个 bucket 就存 MWAA 的东西, 不要跟其他项目混用.
3. 然后它会让你指定一个文件夹用来上传 Dag 源码. 每一个 Python 文件就对应着一个 Dag, 并且 MWAA 会自动检测到更新并在 Airflow UI 中显式出来.
4. 出于网络安全考虑 MWAA 被设定为只能在 Private Subnet 中运行. 因为用来编排的服务器一般都会拥有较高的权限, 放在公网让人直接访问到时非常不安全的, 所以这样设定是合理的. 如果你是 VPC 的老用户, 很清楚如何配置一个至少两个 Public Subnet, 两个 Private Subnet 的网络, 并且 Private Subnet 有一个 Nat Gateway 的网络架构, 你可以参考 `Create the VPC network <https://docs.aws.amazon.com/mwaa/latest/userguide/vpc-create.html>`_ 自己创建. 不然我还是建议直接在 MWAA 的 Console 中选择 "Create MWAA VPC" 选项让系统帮你自动创建.
5. 然后在 "Web server access" 中选择你需要的选项. 作为第一次探索我推荐用 "Public network", 这样你可以直接从 AWS Console login 到 Airflow UI. 而生产环境你肯定是要用 "Private network", 要求必须连 VPN 才能使用.
6. 然后 Security groups 我推荐第一次使用时让 AWS 自动帮你创建. 这取决于你希望从哪里使用 Airflow CLI API 来远程操控 Airflow. 例如你需要从一个 Jump host EC2 上输入 Airflow CLI 命令远程运行一个 DAG, 那么你的 MWAA Security group 就要有对应的 inbound rule 允许 EC2 对其进行访问.
7. 而 PermissionsInfo 这一步则是给 MWAA 对应的权限. 你可以理解为 MWAA 本质上是运行在容器集群上的 App, 如果你希望 Airflow 的执行器能调用 AWS 的 API, 那么 MWAA 就需要有对应的权限. 你可以让 AWS 自动帮你创建. 自动创建的 IAM Role 包含着可用的最小权限, 其中包含了允许对你前面指定的 S3 bucket 进行读写, 能创建以及读写 CloudWatch log group 读写日志, 以及使用 KMS 来对数据进行加密解密.

然后创建 MWAA 的全部时间大约在 30 分钟左右, 30 分钟后你就能用 AWS Console 来登录 Airflow UI 了.

注意, MWAA 不是一个便宜的服务, 最小的 plan 也要 $0.49 / 小时, 也就是 $12 一天, $360 一个月. 你在做完实验之后记得将其关闭.

Reference:

- `Get started with Amazon MWAA <https://docs.aws.amazon.com/mwaa/latest/userguide/get-started.html>`_
- `MWAA Pricing <https://aws.amazon.com/managed-workflows-for-apache-airflow/pricing/>`_


安装 Airflow CLI
------------------------------------------------------------------------------
当 MWAA Environment 被创建之后, 你就该在本地配置对应的开发环境. Airflow 的开发环境主要包含两块:

1. 一个安装了 Airflow 的 Python 环境, 你能在脚本里写 DAG 定义文件.
2. 安装了 Airflow CLI 的程序, 能将 DAG 提交到 MWAA, 并远程运行 DAG.

下面我们详细介绍具体步骤:

1. 由于 Airflow 是用 Python 写的, 它的生态也主要是 Python. 所以按照 Python 开发的规范, 推荐使用 virtualenv 进行开发.
2. Airflow CLI 本身就是一个 Python 库, 你需要选择 Airflow 库的版本以及 Python 的版本. 如果你使用的是 AWS MWAA, 那么推荐你使用跟 Airflow 相对应版本的 Python 版本 (你创建 MWAA environment 的时候就会让你选 Airflow 的版本), 具体的对应关系可以参考 `这篇官方文档 <https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-faqs.html#python-version>`_. 在我们这篇文档中使用的是 Airflow 2.5.1 + Python3.10. 那么你需要在本地安装好 Python3.10. 你如果用的 Mac 或 Linux 则可以考虑用 `pyenv <https://github.com/pyenv/pyenv>`_ 安装.

.. code-block:: bash

    # 创建虚拟环境
    virtualenv -p python3.10 .venv

    # 进入虚拟环境
    source .venv/bin/activate

3. 安装 Airflow CLI 这里有一个小坑. 由于 Airflow 包本身是客户端和服务端一起的, 由于服务端包含了底层实现和 Web App, 它的依赖相当之多. 而 Airflow 版本 + Python 版本的排列组合对应的依赖又不一样, 那么如何确保你的环境中能一定安装成功呢? Airflow 提供了每个 Airflow 版本和 Python 版本的组合下的所有依赖的确定 Version, 官方已经帮你确定了这个依赖组合是没问题的. 请参考下面的命令:

.. code-block:: bash

    # Quick Start
    export AIRFLOW_HOME=~/airflow

    # 输入 airflow 的版本
    AIRFLOW_VERSION="2.5.1"

    # 输入 Python 的版本
    PYTHON_VERSION="3.10"

    # 获得这个官方维护的 constrain file
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

    # 你可以将其打印出来自己看看
    echo $CONSTRAINT_URL

    # 然后再虚拟环境中安装 Airflow
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

Reference:

- `Installation <https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html>`_


使用 Airflow CLI 运行你的第一个 DAG
------------------------------------------------------------------------------
你已经配好了安装环境了, 现在你可以开始写你的第一个 DAG, 然后将它提交到 MWAA 上运行.

首先我们来看这个 Dag 脚本的内容, 请仔细阅读里面的注释:

.. literalinclude:: ./dags/dag1.py
   :language: python
   :linenos:

然后你可以用下面的脚本将你本地的 ``dags`` 目录同步到 S3 上. MWAA 会自动每隔一段时间就去 S3 拉取最新的 DAG 文件. 你也可以在 Airflow UI 中手动点 Refresh.

.. code-block:: bash

    # 将所有的 DAG 文件上传到 S3
    aws s3 sync ./dags s3://807388292768-us-east-1-airflow/dags/ --profile awshsh_app_dev_us_east_1

刷新后你就会在 UI 中看到名为 dag1 的 DAG 了. 点进去后选择 Code, 你就能看到我们的 DAG 代码了. 你可以用这种方式检查 DAG 代码是否是最新的. 然后你就可以用 Actions 里面的运行来手动运行一次 DAG 了.

在生产环境中, 我们一般不会手动运行 DAG. 我们通常会用 Schedule 或是在其他程序中通过 Airflow API 运行 DAG. 下面这个例子给出了用 Python 远程运行 DAG 的代码, 其本质是像 WebserverHost 发送一个 HTTP request 来远程调用位于 MWAA 服务器上的 Airflow CLI. 当然你要确保你运行这段远程执行代码的机器有 IAM 权限 (主要是 ``CreateCliToken``) 并且有 Security Group 网络权限. 请仔细阅读下面脚本中的注释.

.. literalinclude:: ./airflow_cli.py
   :language: python
   :linenos:
