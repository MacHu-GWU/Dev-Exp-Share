Install Ansible
==============================================================================

Ansible 是用 Python 实现的. 你如果熟悉 Python 的话, 你进入 Python 环境, 可以是系统的 Python 也可以是 Virtualenv, 然后 pip install ansible 即可安装成功.

但通常在 Linux 服务器上我们不这么做, 我们通常使用操作系统带的包管理工具安装. 这是因为在服务器上安装合适的 Python 版本本身也很麻烦.

不同的操作系统安装的命令不太一样, 但基本上跟 ``sudo yum install -y ansible`` 这种很类似. 在本学习文档里, 我使用的是 Python 下 virtuaoenv 的安装方式, 这样不会对操作系统本身造成任何影响, 并且删除环境也容易, 删除 venv 所在的文件夹即可.

参考资料:

- Installing Ansible: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html