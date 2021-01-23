#!/bin/bash
# 在 Amazon Linux EC2 上安装 ansible

# Install dependencies
# install git
sudo yum install git -y
# install ansible
sudo amazon-linux-extras install epel -y
sudo yum install ansible -y
which ansible