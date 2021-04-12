
在企业工作时, 有些要求严格的开发组是不允许将 debug 的代码 commit 到 git 仓库的, 所以我推荐用下面的方式对 ansible playbook 进行 debug.

1. 虽然你可以通过 ssh 对目标服务器进行远程执行, 但是直接在跟目标服务器相似的测试虚拟机上进行 debug 肯定要更容易, 并且能够立刻在目标机器上运行命令查看更改是否被应用. 所以我推荐在 AWS 上 launch 一个操作系统以及版本跟目标机器一致的 EC2. 然后 ssh 到里面.
2. 由于你需要将代码

.. code-block:: bash

    #!/bin/bash

    # ssh to EC2
    EC2_PEM="~/ec2-pem/ociso-sanhe-dev.pem"
    EC2_USER="ubuntu"
    EC2_IP="54.144.68.59"
    echo EC2_PEM="${EC2_PEM}", EC2_USER="${EC2_USER}", EC2_IP="${EC2_IP}" && ssh -i ${EC2_PEM} ${EC2_USER}@${EC2_IP}

    # install git
    sudo apt-get install git -y

    # install ansible on ubuntu
    # ref: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu
    sudo apt update
    sudo apt install software-properties-common
    sudo apt-add-repository --yes --update ppa:ansible/ansible
    sudo apt install ansible

    # glone git repo
    GH_TOKEN="put-your-github-personal-access-token"
    git clone https://${GH_TOKEN}@github.com/GSA/odp-packer-ubuntu18.git -b sanhe/dev

    # run playbook on localhost
    ansible-playbook --connection=local --inventory 127.0.0.1 playbook.yml
