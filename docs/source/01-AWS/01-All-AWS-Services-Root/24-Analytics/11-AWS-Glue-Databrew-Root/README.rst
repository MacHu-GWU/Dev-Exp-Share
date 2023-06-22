.. _aws-glue-databrew-root:

AWS Glue Databrew Root
==============================================================================


AWS Glue Databrew 是一个什么样的服务?
------------------------------------------------------------------------------
跟 Databrew 相关的 AWS Glue 是一个 Serverless ETL 服务. 开发者可以用他们熟悉的 PySpark 编程语言编写出能处理任意大小的数据集. 要使用 Glue, 还是需要有一定的编程能力的.

而 Databrew 则是建立在 AWS Glue 之上的一个可视化的, 集数据探索, 数据清洗, ETL 与一身的无代码服务. 我看了这个服务的感觉就是, AWS 还真是 Custom Obsesses. 为了满足非开发者的需要, 专门打造了一个这样的服务, 而且这种创新做的恰到好处, 这种产品思维非常值得借鉴.

虽然它的概念是 "无代码" + "大数据" 处理. 但是还是很难直观的感受到这个产品的优势和价值. 我们在下一章展开说说.


AWS Glue Databrew 的核心概念
------------------------------------------------------------------------------
这里我们假设你已经是有一定经验的 AWS Glue 的用户. 我们来看看 Databrew 中的核心概念和我们熟悉的 Glue 中的概念的联系.

Reference:

- Core concepts and terms in AWS Glue DataBrew: https://docs.aws.amazon.com/databrew/latest/dg/core-concepts-and-terms.html

**Project**

一个项目就是一个 workspace, 类似于 Glue 中的 script.py 的概念, 是为了达到某个目的而创建的项目. 有 input, 有 transformation, 有 output. 只不过期间不用写代码. 你创建了一个 Project 之后就会出现一个类似于 Excel 的界面, 你可以对数据进行探索, 处理.

**Dataset**

一个 Dataset 就是一个二维表. 可以是 Glue Catalog Table, S3 上的文件, 用 JDBC Connection 连接的数据库. Dataset 和 Table 是一一对应的关系. 一个 Project 只能关联一个主 Dataset, 但是可以和多个 Dataset 联动进行数据分析.

**Recipe**

类似于你在 Excel 中进行数据分析, 对数据进行的任何处理动作都被视为一个 Action. 例如对数据进行过滤, 删除一个 Column, 重命名一个 Column, 对 Column 进行函数计算, 和其他表 Join. 而你对数据的处理过程会被序列化为一系列的 Action, 这些 Action 合起来就组成了一个 Recipe.

**Job**

一个 Job 就相当于一个 Glue Job. 它以 Dataset 为输入, Receipt 为其中的 ETL 逻辑, 生成一个新的 Dataset 为输出.

**Data lineage**

数据血统.

**Data profile**

数据概要. 例如数据的分布, 数据的类型, 数据的缺失情况等等.


AWS Glue Databrew 的底层逻辑
------------------------------------------------------------------------------
根据以上的核心概念可以看出. AWS 将数据源抽象成了 Dataset, 将 ETL 程序和业务逻辑抽象成了 Recipe, 将运算环境抽象成了 Job, 然后把所有的这些都放在一个可视化的 Project 关联起来进行操作. 非开发者用户只需要点点鼠标就能创建 Dataset, 而无需了解数据库连接等知识. 只需要在 Project 的图形化界面中对数据进行拖曳, 点击, 这些动作就会被记录为 Action 而形成 Recipe. 然后点击运行, 无需了解 PySpark 的命令行启动, 就可以启动一个 Job 进行数据处理. 由于底层使用的还是 Glue, 所以它可以胜任任意规模的数据集处理.

我第一次看到这个设计之后非常感慨.


AWS Glue Databrew 的费用
------------------------------------------------------------------------------
Databrew 的费用主要分两块.

1. 在 Project 中进行数据分析的费用. 每 30 分钟 $1, 不够 30 分钟的部分按 30 分钟算 (收费粒度有点粗). 由于 Project 其实是一个暂存区, 它是为了你工作提供了一个界面. 最终你探索完之后, ETL 的逻辑还是要保存为 Recipe 的. 但是它还是需要 Provision 后台的计算资源, 而且这个计算资源还不能太小 (内存得够大), 所以这个费用还是比较高的.
2. 你运行 Databrew Job 所用的 ETL 费用. 每个 Data Node $0.48 一小时, 精确到分钟. 这跟 Glue 一样, 启动了多少个节点, 运行了多久, 就收费多少.

Reference:

- `AWS Glue Pricing <https://aws.amazon.com/glue/pricing/>`_


Databrew 所支持的 Dataset
------------------------------------------------------------------------------
- 对于直接存放在 S3 上的文件, Databrew 支持 csv, json, excel, orc, parquet 这几种流行的数据格式.
- 对于已经被 Glue Catalog 所连接的数据, 直接用 Glue Catalog 即可.
- 对于需要用 JDBC 直连的数据库类数据源, Databrew 支持以下数据源:
    - Microsoft SQL Server
    - MySQL
    - Oracle
    - PostgreSQL
    - Amazon Redshift
    - Snowflake Connector for Spark

Reference:

- Connecting to data with AWS Glue DataBrew: https://docs.aws.amazon.com/databrew/latest/dg/datasets.html


连接位于 VPC 中的资源
------------------------------------------------------------------------------
有些资源 (例如数据库) 是位于 VPC 中的, 那么你的 Databrew 也要放在 VPC 中才能与之通信. 当你在探索数据的时候, Project 本身是不需要任何 VPC 设置的, 你的 VPC 相关设定是在定义 Dataset, 创建 Glue Catalog 的时候创建的. 总之

Reference:

- Using AWS Glue DataBrew with your VPC, Using AWS Glue DataBrew with VPC endpoints: https://docs.aws.amazon.com/databrew/latest/dg/infrastructure-security.html


我们来看一个具体的例子
------------------------------------------------------------------------------
TODO

.. literalinclude:: ./example.py
   :language: python
   :linenos:
