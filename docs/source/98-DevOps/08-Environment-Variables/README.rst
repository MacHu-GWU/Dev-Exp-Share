Environment Variables
==============================================================================


在 Linux 系统中不同级别的 Env Var
------------------------------------------------------------------------------
在 Linux 的大多数发行版都有有下面几个文件和环境变量有关:

- ``/etc/environment``: 全系统级的环境变量, 只读文件, 对所有登录的用户生效. 内容格式如下::

    MY_VAR="MY_VALUE"

- ``/etc/profile``: 用户级的环境变量, 只读文件, 只对指定用户生效. 内容格式如下::

    export MY_VAR="MY_VALUE"

- ``~/.bashrc``: shell session 级别的环境变量, 当前 ``~`` 用户可读写, 每次进入一个新的 sh / bash session 时生效. 内容格式如下::

    export MY_VAR="MY_VALUE"

这里引用一个 Stackoverflow 上面的解释:

- ``/etc/environment``: This file is specifically meant for system-wide environment variable settings. It is not a script file, but rather consists of assignment expressions, one per line. Specifically, this file stores the system-wide locale and path settings.
- ``/etc/profile``: This file gets executed whenever a bash login shell is entered (e.g. when logging in from the console or over ssh), as well as by the DisplayManager when the desktop session loads.


为你的 App Runtime 应用运行时配置 Env Var
------------------------------------------------------------------------------
一般一个 App 的运行环境本身是被虚拟化的. 这个运行环境的本身的环境变量不应该被 App 所管理, 而是应该被运行环境本身管理.

举例来说, AWS 有 EC2 虚拟机, ECS 容器, Lambda 临时容器 这几种运行环境. 对于 EC2 有 User Data 可以在启动的时候自动配置 Env Var, ECS 有 Task Definition 可以定义 Env Var, Lamdba 也有 Env Var 定义. 如果是你自己定义的容器, 同样也可以在 Dockerfile 中定义 Env Var. 其中 ECS, Lambda, Docker 这几种情况比较简单, 就是简单的定义 Key Value 即可. 这里我们详细讲一下 **如何为 EC2 配置系统全局的 Env Var**:

``/etc/environment`` 文件只读, 你需要用 sudo 身份对其进行修改. 而这个步骤我们希望将其自动化. 一般我们给一个文件的末尾加一行是用 ``echo "a line here" >> file.txt`` (注意是 ``>>``, 这是给末尾加一行, 而如果是 ``>`` 则是完全覆盖整个文件) 而 ``echo`` + ``>>`` 涉及到了输入输出重定向, 这种操作是无法和 sudo 共同使用的. 你可以用 echo 将内容输出到一个临时文件, 然后用 cp 命令对源文件进行覆盖.

ec2

ssh -i "~/ec2-pem/aws-data-lab-opensource/us-east-1/aws-data-lab-opensource-sanhe-dev.pem" ec2-user@52.90.40.102


https://stackoverflow.com/questions/34205532/how-to-set-environment-variables-on-ec2-instance-via-user-data





Ref:

- Ubuntu Help - EnvironmentVariables: https://help.ubuntu.com/community/EnvironmentVariables
- Linux Environment.d: https://www.man7.org/linux/man-pages/man5/environment.d.5.html
- EC2 User Data: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts

.. code-block:: bash

    #!/bin/bash
    # not work in ssh, not work in user data
    sudo echo "MY_VAR=\"MY_VALUE\"" >> /etc/environment

.. code-block:: bash

    #!/bin/bash
    # work in ssh, not work in user data
    echo export MY_VAR="MY_VALUE" | sudo tee -a /etc/environment

.. code-block:: bash

    #!/bin/bash
    # work in ssh, not work in user data
    rm /tmp/user-etc-environment
    echo "MY_VAR=\"MY_VALUE\"" >> /tmp/user-etc-environment
    sudo cp /tmp/user-etc-environment /etc/environment


#!/bin/bash
# work in ssh, not work in user data
echo "CATHY_NAME=\"cathy\"" >> /tmp/user-etc-environment
sudo cp /tmp/user-etc-environment /etc/environment
