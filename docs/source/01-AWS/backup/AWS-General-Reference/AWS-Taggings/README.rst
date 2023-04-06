AWS Tagging
==============================================================================


Summary
------------------------------------------------------------------------------
Tag 是 AWS Resource 的 Metadata, 是一组 Key-Value 的键值对. 通过 Tag, 可以对 AWS 的资源进行分类, 统计, 管理, 鉴权等操作. 强烈建议你的公司按照一定的 schema 打 Tag, 用 AWS Organization Tag Policy 来强制要求 Developer 为 AWS 资源打上合适的 Tag.

Reference:

- Tagging AWS resources: https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html
- Tagging Best Practice: https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html


Tagging Best Practice
------------------------------------------------------------------------------
你的 Tag 要尽量为你的目标服务, 比如我们可以用 Tag 来实现如下目标:

- Technical Tags:
    - Name – Identify individual resources
    - Application ID – Identify resources that are related to a specific application
    - Application Role – Describe the function of a particular resource (such as web server, message broker, database)
    - Cluster – Identify resource farms that share a common configuration and perform a specific function for an application
    - Environment – Distinguish between development, test, and production resources
    - Version – Help distinguish between versions of resources or applications
- Automation:
    - Date/Time – Identify the date or time a resource should be started, stopped, deleted, or rotated
    - Opt in/Opt out – Indicate whether a resource should be included in an automated activity such as starting, stopping, or resizing instances
    - Security – Determine requirements, such as encryption or enabling of Amazon VPC flow logs; identify route tables or security groups that need extra scrutiny
- Business:
    - Project – Identify projects that the resource supports
    - Owner – Identify who is responsible for the resource
    - Cost Center/Business Unit – Identify the cost center or business unit associated with a resource, typically for cost allocation and tracking
    - Customer – Identify a specific client that a particular group of resources serves
- Security:
    - Confidentiality – An identifier for the specific data confidentiality level a resource supports
    - Compliance – An identifier for workloads that must adhere to specific compliance requirements

我自己研究的时候, 也是按照这个 schema 来打 Tag 的.

- technical tags:
    - ``tech:project_name``:
    - ``tech:env_name``: dev, staging, prod, etc ...
    - ``tech:version``: semantic version, 通常用来管理 deployment 的版本
    - ``tech:human_creator``: 谁创建的?
    - ``tech:machine_creator``: 谁用什么工具创建的?
- automation tags:
    - ``auto:active_time``: 可以用来标志一个机器在什么时候保持启动状态, 可以参考 `CRON expression <https://docs.oracle.com/cd/E12058_01/doc/doc.1014/e12030/cron_expressions.htm>`_. 例如你定义服务器每周 1-5 的 8AM 到 8PM 保持开机, 其他时候自动关机.
    - ``auto:delete_at``: 可以用来标志一个机器什么时候需要被定时删除.
- business tags: 通常这种 tag 是用来 track cost 的, 这样你就可以按照 ou, team, project 来统计分别花了多少钱了.
    - ``bus:ou``: organization unit name (department name)
    - ``bus:team``: team name
    - ``bus:project_name``:
    - ``bus:owner``: 谁来负责这个 resource? 通常是一个 email.
    - ``bus:user``: 谁在使用这个 resource? 通常是几个 team 的名字或是几个 email.
- security tags:
    - ``sec:confidentiality``: public, confidential, secret, top secret, etc ...
    - ``sec:compliance``: HIPAA, PCI, etc ...

AWS Organizations 是一个用来管理企业内多个 AWS Accounts 的服务. 其中有一个功能是 `Tag Policies <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html>`_, 可以标准化你的 Tag Schema, 比如可以定义某个 Tag Key 对应的值必须是几个选项中的一个. 比如可以做到如果 Tag 不合规你就不允许创建, 也可以做到 Tag 不合规还是允许创建, 不过会发 Alert 给创建的人.

Reference:

- Tagging categories: https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html#tag-categories
- AWS Organizations Tag policies: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html


Tag Naming Limits and Requirements
------------------------------------------------------------------------------
简单来说有下面这些限制:

- 一个 resource 最多打 50 个 user defined tag.
- key 最多 128 个字符, value 最多 256 个字符, value 可以是空字符串.
- 允许你用 ``-``, ``.``, ``:``, ``/``, ``=``, ``+``, ``-``, ``@`` 这些字符. 这里有一些约定俗成的规律, 例如 key 里最多用 ``-``, ``_``, ``:``, 通常 ``:`` 是用来做分隔符的. value 里可以随便用. key 的 naming 推荐要么 Camel Case, 例如 ``ProjectName``. 要么 Slug 或 Snake Case, 例如 ``project-name``, ``project_name``. 如果有层级结构则用 ``:`` 做分隔符, 例如 ``my-corp:IT:dev:project-name``.

Reference:

- Tag naming limits and requirements: https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html#tag-conventions