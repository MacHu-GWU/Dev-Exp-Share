Apache Airflow
==============================================================================

.. contents::
    :depth: 1
    :local:


基础篇
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


What is Airflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Airflow 是由 Airbnb 公司开发, 后来捐献给 Apache 软件基金会的开源项目.

Airflow 是个 Workflow Orchestration (工作流编排) 的 Service (服务).

Workflow (也叫 工作流) 是一个由多个 Task (也叫 任务) 按照顺序和依赖关系组成的.

你有几个 Task 要做, 可能是执行一段代码, 远程执行服务器上的程序 或是任何事情. 这些 Task 之间有互相依赖的关系. 有的 Task 需要其他 Task 成功完成后才能开始. 有的 Task 成功或是失败后执行不同的 Task. 有的 Task 需要并行或者串行执行. Task 之间还可能互相传递参数. 失败后有的需要重试.

那么当 Workflow 中的 Task 很多, 之间的关系又非常复杂时, 能稳定的按照逻辑执行下来并记录日志和状态就不是很容易了.

Airflow 是一个 Python 写的服务器, 允许你以单点或是集群, 虚拟机或是容器的方式部署. 同时 Airflow 也是一个 Python 库, 允许你用 Python 方便滴定义你的 Workflow 以及 Task, 然后 Submit 到 服务器上定时运行. 并且这个服务器还自带 UI 界面, 可以方便的查看你的 Workflow 的状态以及日志. 当然命令行工具以及 Python 运行也都是允许的.

这就叫做 Workflow Orchestration.

本质上 Airflow 的很多功能和 AWS Step Function 是重合的, 不过 Airflow 更加通用, 且更加被业内所广泛使用.


Air Flow 的 核心组件和概念
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Web Server: 一个 Web UI 的服务器组件
- Scheduler: Airflow 调度器, 决定了什么时候, 分配哪个 Executor 来执行哪个 Workflow. 内部 Airflow 有一个 Message Queue 来管理事件的触发, 比如触发执行任务.
- Executor: Airflow 执行器, Workflow 和 Task 会被交给 Executor 来执行, 本质上是一个进程.
- Database: Airflow 需要连接到一台 SQL Database 来保存状态数据, 在集群部署时也是中心化的状态数据存储.
- DAG: 有向无环图. Workflow 在程序上的抽象就是一个 DAG. 你只要定义了每个 Node 和 Edge, 那么你的 Workflow 的逻辑也就出来了. 每个 Node 有很多 Attribute, 比如 Id, Argument. 每个 Workflow 最终就是一个 ``.py`` 文件, 里面必须要有一个 DAG 的实例.
- Operator: Operator 就是在 python code 里的实现, 是一个类. 每个 Task 本质上就是一个 Callable 的函数, 可以抛出异常, 可以休眠, 可以重试.


AWS MWAA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

全称是 AWS Managed Workflows for Apache Airflow. 我们简称 AWS Airflow. 是 AWS 的一个 Airflow 托管服务. 允许你一键部署 Airflow 集群, 并且自带数据库和UI. 从 AWS S3 读取 dag 文件, 以及依赖包, 还有 requirements.txt 文件. 并且和 AWS 自带的

出于安全考虑, AWS Airflow 只能部署部署在 Private Subnet 上. 并且 AWS 会自动帮你配置好 Web UI 的 Endpoint, 基于 IAM Role 控制访问 Web UI 的权限. 并且用 IAM Role 来管理 Airflow 对 AWS 资源的访问权限.


Links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Airflow Doc: https://airflow.apache.org/docs/apache-airflow/stable/index.html
- AWS MWAA Doc: https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html


实战篇
------------------------------------------------------------------------------
.. autotoctree::
    :maxdepth: 1
    :index_file: README.rst
