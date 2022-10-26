
Amazon Linux
==============================================================================
Keywords: AmazonLinux, amz

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Identify Amazon Linux Images
------------------------------------------------------------------------------
如何鉴别当前的 OS 是 Amazon Linux:

1. 检查 ``/etc/image-id``文件, 包含了镜像文件的详细信息. 该文件是只读的, 只有 root 能修改::

    # output of: ``cat /etc/image-id``
    image_name="amzn2-ami-kernel-5.10-hvm"
    image_version="2"
    image_arch="x86_64"
    image_file="amzn2-ami-kernel-5.10-hvm-2.0.20220606.1-x86_64.xfs.gpt"
    image_stamp="c37a-c4d4"
    image_date="20220613185348"
    recipe_name="amzn2 ami"
    recipe_id="30341f50-8334-65d7-ca02-666d-0439-5d44-f5ae3eab"

2. 检查 ``/etc/system-release``文件, 包含了简要的发行版信息. 该文件是只读的, 只有 root 能修改::

    Amazon Linux release 2 (Karoo)


Package Manager
------------------------------------------------------------------------------
Amazon Linux 源于 Fedora, 用的是 ``yum`` 包管理, 源也是跟 Fedora 一样的由官方维护的 ``yum`` 源. Amazon Linux 也配置了 Extra Packages for Enterprise Linux (EPEL) 用于由社区提供的第三方包, 但是默认没有启用. 你可以用以下命令启用它::

    sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

同时 ``amazon-linux-extras`` 命令允许安装额外的

- Amazon Linux Package Repository: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-linux-ami-basics.html#package-repository


Reference
------------------------------------------------------------------------------
- Amazon Linux: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-linux-ami-basics.html#amazon-linux-cloud-init


