git clone Access Private Repo (使用 git 访问私有仓库)
==============================================================================

.. contents::
    :local:


使用 SSH 在不手动输入账号密码的情况下操作 Private Repo
------------------------------------------------------------------------------

- Q: 有哪些方法可以在不弹出输入框的情况下使用 git 命令拉取 private repo? 这样就可以编写自动化脚本了.
- A: 常用的有两种:
    1. 使用 ``git clone 'https://<username>:<password>@github.com/<username>/<repo-name>.git'`` 命令. 将账号密码编码成命令中的一部分. **有很大风险且, 不推荐**.
    2. 配置好 SSH Key 之后, 使用 ``git clone git@github.com:<username>/<repo-name>.git``. **该方法适用于人工使用 git 命令的情况**.
    3. 配置好 Personal Access Token 之后, 使用 ``git clone https://<personal-access-token>@github.com/<username>/<repo-name>.git``. **该方法适用于自动化系统使用 git 命令的情况**

- Q: 为什么不推荐第一种?
- A: 因为这样需要将账号密码明文存储在脚本里, 这样非常危险. 而且很多机器上的命令行会保留日志, 也会使得账号密码明文保存在日志里.

- Q: 为什么第二种不错?
- A: 因为你创建的 SSH 可以随时在 GitHub 上删除, 而且位于你 ``$HOME/.ssh/id_rsa`` 的 私钥 无法被其他系统用户访问. 只要 私钥 不泄露, 那么就是安全的.

- Q: 为什么第三种也不错?
- A: 因为你创建的 Token 保存在 GitHub 上, 且你自己也可以用密码管理软件妥善保存. 而这个 Token 是用于第三方系统与 GitHub 集成的, 比如 CICD 系统. 而且 GitHub 允许设定 access token 的权限, 可以实现比 SSH 更精细的权限控制.


使用 SSH
------------------------------------------------------------------------------

1. 生成一对私钥和公钥, 默认私钥放在 ``$HOME/.ssh/id_rsa``, 公钥 ``$HOME/.ssh/id_rsa.pub``. (参考 Generating a new SSH key and adding it to the ssh-agent: https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

.. code-block:: bash

    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

2. 将公钥交给 GitHub, 点击这个链接 https://github.com/settings/keys 创建 ``New SSH Key`` 即可.
3. 然后使用 ``git clone git@github.com:<username>/<repo-name>.git`` 通信.


使用 Personal Access Token
------------------------------------------------------------------------------

.. code-block:: bash

    export MY_GIT_TOKEN="56d5ec6b578a89f41ec25c523250f832a50a55fb"
    git clone https://${MY_GIT_TOKEN}@github.com/MacHu-GWU/test-private-repo
