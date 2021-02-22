Ansible
==============================================================================

.. contents::
    :depth: 1
    :local:

Ansible 是一个用 Python 实现的, 基于 SSH 的服务器配置工具. 简单来说, 服务器配置就是一系列的 拷贝和下载文件, 运行命令. 而 Ansible 用 Inventory 来批量管理服务器, 用 Playbook 来编排你要执行的动作, 然后使用 ansible cli 来选择对哪些服务器, 按照什么样的顺序, 执行哪些定义好的动作. 这就是 Ansible 的主要功能.


Quick Links
------------------------------------------------------------------------------

入门:

- Inventory Intro: https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory
- Playbook User Guide: https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html

常用手册:

- Command Line Reference: https://docs.ansible.com/ansible/latest/user_guide/command_line_tools.html
- Ansible Built-in Collecton Index: https://docs.ansible.com/ansible/latest/collections/index.html


Ansible 的重要概念
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:


Inventory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

一个 .ini 或是 .yml 文件, 定义了你想要管理的服务器, 当然是要给定 DNS name 或是 IP 地址来指定服务器. 这里服务器可以按照层级进行分组, 以便于你用命令指定你要将 Playbook 在哪些机器上执行. 而这里的 DNS name 或 IP 地址可以是用形如 ``www[01:50].example.com`` 的模式来一次指定多台. 也可以用 dynamic inventory 来用一段程序来定义一个逻辑上的 多台服务器. 例如 用 Tag 来选择 AWS EC2.

详细内容请参考:

- How to build your inventory: https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
- Dynamic inventory: https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html
- Dynamic inventory plugin for aws_ec2_inventory: https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html


Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collection 实际上就是第三方的 Plugin, 相当于编程语言的第三方库. 例如 Python 的 Library. Ansible 用来托管 Collection 的平台叫做 ansible galaxy https://galaxy.ansible.com/home. 你可以在上面 查找, 下载, 发布 你的 Collection.


Playbook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Playbook 定义了你在服务器上执行的操作. 其中有两个子定义 Task 和 Play. Tast 就是一些具体的操作, 例如运行 shell script, 运行 command, 拷贝文件 等. 是比较小的逻辑单元. Play 则是按顺序包含了许多 Task, 是一个比较大的逻辑单元. 而一个 Playbook 里包含了许多 Play.


Ansible 实战 - Inventory
------------------------------------------------------------------------------

参考资料:

- Intro Inventory: https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory

Inventory file 支持 .yml 和 .ini 两种格式. 显然 .ini 已经过时了, 我们不去学习他.

我们来看一个最简单的例子:

.. code-block:: yaml

    all: # a group name
      hosts:
        mail.example.com:
      children:
        webservers: # a group name
          hosts:
            foo.example.com:
            bar.example.com:
        dbservers: # a group name
          hosts:
            one.example.com:
            two.example.com:
            three.example.com:

Inventory 管理服务器是通过 Group (组) 来实现的. 简单来说一个 Group 包含了 一到多 台机器. 一台机器可以被多个 Group 所包含. 而 Group 内可以定义 Variables 变量, 例如 ansible 内置的变量 ``ansible_user`` 用来指定远程用户名, ``ansible_ssh_private_key_file`` 用来指定 SSH 的密钥文件. 也可以自行定义变量, 例如 ``http_port``.

当你在运行 playbook 的时候, 你需要在 playbook 的 yml 文件中指定 group. 被指定的 group 中的 hosts 会被 playbook 更改.

**有两个默认的隐藏 Group, all, ungrouped. 所有的 host, 无论是否定义了 group name, 都会被包含在 all 这个 group 中. 而 ungrouped 则是哪些没有定义在 group name 下, 直接以 ip 地址的形式定义的所有 host**.

**而 group 之间又有 children 的概念. 所有的 group 会自动包含他们的 children 中定义的 hosts**. 所有的 children group 也同样是 group, 可以在 playbook 中被指定. 在定义的时候请注意避免循环, 不能两个 group 互为对方的 children. 结合前面介绍的 Variables, 值得注意的是, 如果 children 和 parent 中都定义了同一个 variable, 那么以 children 的为准. 这就跟编程语言中的继承关系一样.

下面我们来看一个更复杂的例子, 在该例子中, 我们的分组逻辑是按照 what, where, when 来分组的. 而在 prod, test 组中我们就使用了 children 来避免重复定义 host.

.. code-block:: yaml

    all: # default Group name, will include all hosts appears in this file
      hosts:
        mail.example.com:
    amazonEcommerce: # amazonEcommerce 是一个 group name, 由用户指定
      children: # children 是一个 ansible 内置的 declaritive, 表示下面的 key 都被视为一个 group
        # What - An application, stack or microservice (for example, database servers, web servers, and so on).
        webservers:
          hosts:
            foo.example.com:
            bar.example.com:
        dbservers:
          hosts:
            one.example.com:
            two.example.com:
            three.example.com:
        # Where - A datacenter or region, to talk to local DNS, storage, and so on (for example, east, west).
        east:
          hosts:
            foo.example.com:
            one.example.com:
            two.example.com:
        west:
          hosts:
            bar.example.com:
            three.example.com:
        # When - The development stage, to avoid testing on production resources (for example, prod, test).
        prod:
          children:
            east:
        test:
          children:
            west:


Ansible 实战 - Playbook
------------------------------------------------------------------------------

Pre installed plugin: https://docs.ansible.com/ansible/latest/collections/index.html

Ansible Playbook 是 Ansible 的核心, 定义了配置服务器的各种操作.

我们来看一个例子:

.. code-block:: yaml
    # content of host.yml
    ---
    all:
      hosts:
        111.111.111.111:
      vars:
        ansible_user: ec2-user
        ansible_ssh_private_key_file: ~/my-key-pair.pem

.. code-block:: yaml

    # content of playbook.yml
    # this is a PLAY
    - name: action1
      hosts: all
      # this is a TASK
      tasks:
      - name: create a test.txt file
        shell: |
          echo "hello" > ~/test.txt

上面这个例子的功能是在 AWS 的一台 EC2 上, 创建一个内容为 ``hello`` 的 ``$HOME/test.txt`` 文件. 从语法上拉看, playbook 是一种 declaration language (声明式语言), 每一个 YAML 的 Key 都是由 ansible 实现的, 具有特殊的含义. 而用户主要负责填写 Value 来控制 playbook 的行为.

从结构上来看, **一个 playbook 包含了很多个 ``PLAY``, 一个 ``PLAY`` 包含了很多个 ``TASK``, 而每个 ``TASK`` 就是对服务器进行一些具体的操作**, 功能的逻辑上通常不会很复杂, 不过具体的实现可以是一个简单的 单条命令, 也可以是一个非常复杂的 bash script. ``TASK`` 是 Playbook 的最小操作单位, 例如运行一些命令. 而 ``PLAY`` 则是一个比较大的逻辑概念, 比如安装, 初始化, 配置某个软件.

下面这条命令即可将 playbook 中定义的操作, 在远程机器上执行:

.. code-block:: bash

    ansible-playbook playbook.yml -i host.yml

这里我们还提供了两个例子. 第一个是使用了 自定义的 group name; 第二个是是用来在 Children 中定义的 group name; 他们都可以在 playbook 中被引用.

.. code-block:: bash

    ansible-playbook playbook-example-1.yml -i ./host-example-1.yml
    ansible-playbook playbook-example-2.yml -i ./host-example-2.yml


Ansible 实战 - Collection
------------------------------------------------------------------------------

多数的 Collection


Ansible 实战 - CLI
------------------------------------------------------------------------------

.. contents::
    :depth: 1
    :local:

理解 ansible 命令行如何工作
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

由于 Ansible 本质上是一个 Python 命令行程序. 通常 DevOps 工程师电脑上的 ansible 是系统级的 ansible. 也就是工程师用 package manager, 例如 Redhat 和 CentOS 上的 ``yum install ansible``, Ubuntu 上的 ``apt-get install ansible``, MacOS 上的 ``brew install ansible``.

而我们知道 Linux 系统上的工具对于不同的 User 是区分开来的. 例如以 Root 安装的工具其他 User 通常能使用, 例如 git. 而以其他 User 安装的工具 Root 通常不能使用, 这事为了避免用户安装的可执行文件对系统造成损害. 所以当你再打 ``ansible`` 命令时, 你要知道你实际上在用的哪个 ``ansible``. 你可以用 ``which ansible`` 来查询.

如果你熟悉 Python 里的 Virtualenv 的话, 你会知道你同样可以用 ``pip install ansible`` 来安装 ``ansible`` 而这个 ``ansible`` 要在同样的 Python 环境中才能使用. 例如你进入了 virtualenv 再 ``pip install ansible`` 那么你在 virtualenv 之外是无法使用的.


``ansible-config``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ansible.cfg`` **File**

``ansible.cfg`` 文件控制了 ansible 的许多行为, 比如 SSH 的行为, 在哪里寻找特定文件等. 而当你执行 ansible cli 时, 你用到的是哪一个 ``ansible.cfg`` 文件呢? Ansible 默认会按照下面的顺序寻找 ``ansible.cfg`` 文件, 如果找到了, 就不去后面的位置找了. 顺序是这样的:

- ``ANSIBLE_CONFIG`` (environment variable if set)
- ``ansible.cfg`` (in the current directory)
- ``~/.ansible.cfg`` (in the home directory)
- ``/etc/ansible/ansible.cfg``

``ansible-config`` 是一个命令行工具, 允许你:

- ``ansible-config list`` 列出所有可用的选项.
- ``ansible-config view`` 显示当前被使用的 ``ansible.cfg`` 文件内容
- ``ansible-config dump`` 将你当前的 config, dump 成为新的 ``ansible.cfg`` 文件, 或是与已经存在的 ``ansible.cfg`` 文件中的选项合并, 如果已经存在某个 KEY, 则覆盖之.

相关文档:

- Configuring Ansible: https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html
- Ansible Configure Settings: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings
- ``ansible-config`` CLI: https://docs.ansible.com/ansible/latest/cli/ansible-config.html#ansible-config


