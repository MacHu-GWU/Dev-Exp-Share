.. _aws-vpc-vpn-endpoint:

VPN Endpoint
==============================================================================
Keywords: AWS VPC, VPN Endpoint

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


VPN Endpoint 是做什么的?
------------------------------------------------------------------------------
我们已经知道 AWS VPC 是企业私有网络服务. 当你把很多服务例如 数据库, 容器 部署在 VPC 内部时, 你如果想要用家里或是办公室的网络和电脑连接到位于 VPC 中的资源, 通常有这么几种做法:

1. 在 AWS 上开一个 EC2 或 Cloud9 作为跳板 (Jump Server), 将其放在 VPC 内, 然后 SSH 上去, 然后从 EC2 上对 VPC 中的资源发起请求.
    - 缺点: EC2 或者 Cloud9 中的开发环境没有本地友好.
2. 对于大型企业, 一般会让 ISP (网络服务提供商) 将企业内网用 Direct Connect 直接拉一条专线到 AWS, 所有跟 AWS 交互的资源都直接走专线而不经过公网.
    - 缺点: 个人可负担不起
3. 用 AWS VPN Endpoint 服务为 VPC 创建一个 VPN Endpoint, 相当于你可以登录 VPN 后就相当于连接到了 VPC 以内.
    - 优点: 简单方便, 很快就能创建好
    - 缺点: 每次使用要登录

综上, 你要想让普通电脑或者任意软件环境连接到 VPC 内, 同时又不想维护复杂的网络基础设施. 使用 AWS VPN Endpoint 是最佳选择.


使用 VPN Endpoint 所需的前提条件
------------------------------------------------------------------------------
1. 你已经设置好了 VPC, 至少有 public subnet. private subnet 是为了部署数据库等服务所准备的, 所以对于 VPN 来说无所谓.
2. 创建了 AWS Managed Microsoft AD, 用于验证身份, 鉴权. 后面会说如何设置.
3. 创建了 Server 和 Client 的 Certificate 用于通信加密, 并导入到 AWS Certificate Manager (ACM) 中方便管理.
4. 创建了 VPN Client Endpoint. 并 Associate 了 Subnet, 以及设置了 Authorization, 并下载了 VPN Endpoint 用于登录的 config 文件, 用于在 OpenVPN 客户端中一键登录. 这一步骤是最关键的.
5. 为你的 VPC 配置了 DHCP (动态主机配置协议), 这样才能让你登陆 VPN 后自动获得 VPC 内网的一个 IP 地址.


VPN Endpoint 鉴权
------------------------------------------------------------------------------
连接到 VPN 的时候, 如何知道请求发起人是有权限的呢? 这里涉及两个概念:

1. Authentication (身份验证): 证明你是谁.
2. Authorization (鉴权): 当知道你是谁之后, 验证你是否有权限做某事.

根据这篇文档 `Client Authentication <https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html>`_ AWS Client VPN 支持以下三种身份验证方法:

- Active Directory authentication (user-based): AD 是微软在 1990 年代的企业身份验证解决方案. 主要是通过为企业里的每个人一个 Email / Password 作为一个账户. 由于历史原因, 该方案在企业内极其流行. 由于 VPN 的使用者往往是在 AWS 外, 不可能用 IAM, 而用 AD 的人又那么多, 所以该方案是首选方案.
- Mutual authentication (certificate-based): 该方案基于 Certificate, 也就是 Https 协议里的那个根证书. 要求服务器 (VPN Endpoint 端) 导入了 server certificate, 而客户端机器上要有 client certificate. 该方式需要为 client 配置 certificate, 通常用于服务器之间的身份验证, 不推荐作为实体人用户的解决方案.
- Single sign-on (SAML-based federated authentication) (user-based): 随着历史的发展, 又有了很多提供身份验证的公司比如 Okta, OneLogin 等, 提供低成本的 AD 的替代.

所以对于大部分个人 AWS 用户, 没有资源和精力配置 SAML, 直接使用 AWS Directory Service 是最好的选择. 因为该服务提供了多种 AD, 其中最为亮眼的是 Microsoft AD 和 Linux 对应的 Simple AD. Simple AD 致力于提供和 Microsoft AD 一样的使用体验, 但是价格只有前者的一半.

在之后配置 VPN Endpoint 的过程中, 你需要指定使用 AD 来鉴权. 你每次在电脑上用客户端软件登录 VPN 的时候需要输入账号密码. 这样 VPN Endpoint 才能知道你是谁.



配置 VPN Endpoint - 1. 创建 AWS Simple Active Directory
------------------------------------------------------------------------------

这一步是为你的 VPN 创建用户池以及账号密码管理.


创建 AWS Managed MicroSoft AD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**创建**

- 前往 `AWS Active Directory Console <https://console.aws.amazon.com/directoryservicev2/identity/home?#!/directories>`_ -> 点击 ``Set up directory`` -> ``AWS Managed MicroSoft AD``
- 参照官方文档 `Create your AWS Managed Microsoft AD directory <https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_getting_started_create_directory.html>`_, 创建 Simple Active Directory:
    - Edition = Standard Edition
    - Directory DNS Name = ``sanhe-infra-dev.vpn-users.com`` 其实无所谓, 一个 AWS 账号内不重复即可
    - Directory NetBIOS name = ``VpcUsers`` <= 15 characters 一个短名字.
    - 请确保 AD 放在了 Public Subnet 上.
    - 默认的 Admin Username 是 ``admin``


创建 AWS Simple Active Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**创建**

- 前往 `AWS Active Directory Console <https://console.aws.amazon.com/directoryservicev2/identity/home?#!/directories>`_ -> 点击 ``Set up directory``
- 参照官方文档 `Tutorial: Create a Simple AD directory <https://docs.aws.amazon.com/directoryservice/latest/admin-guide/simple_ad_tutorial_create.html>`_, 创建 Simple Active Directory:
    - Directory DNS Name = ``sanhe-infra-dev.simple-directory-vpn.com`` 其实无所谓, 一个 AWS 账号内不重复即可
    - Directory NetBIOS name = ``VpcUsers`` <= 15 characters 一个短名字.
    - 请确保 AD 放在了 Public Subnet 上.
    - 默认的 Admin Username 是 ``Administrator``


添加用户
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果只有你一个人用, 使用 Admin 账户也可以. 如果有多个用户需要共享这个 VPN, 那么你需要为他们创建不同的 用户名 密码.

具体方法请参考官方文档 `Manage users and groups in Simple AD
 <https://docs.aws.amazon.com/directoryservice/latest/admin-guide/simple_ad_manage_users_groups.html>`_.


配置 VPN Endpoint - 2. 创建并导入 Server Certificate
------------------------------------------------------------------------------
无论你的鉴权方式是什么, 你的 VPN Endpoint 需要有 Certificate (不然 network traffic 很容易被拦截和篡改).

对于一个 AWS Account, 只要 Server 和 Client 分别有 Server 和 Client 的 Certificate 就能互相信任通信. 你创建很多套也是可以的.


用 Cloud9 创建并 Import Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这一步是用 easy-rsa 开源标准创建 Certificate. 该操作建议在 Cloud9 上的 Linux 的命令行中进行 (windows 对命令行工具不友好, macos 上有些依赖不一定满足, 不如 linux 稳定可控). 以下内容全部来自于官方文档 `Mutual authentication <https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html#mutual>`_

1. Clone the OpenVPN easy-rsa repo to your local computer and navigate to the ``easy-rsa/easyrsa3`` folder.

.. code-block:: bash

    # 拉取源代码
    git clone https://github.com/OpenVPN/easy-rsa.git

    # 进入到 easyrsa3 目录
    cd easy-rsa/easyrsa3

2. Initialize a new PKI environment.

    ./easyrsa init-pki

3. To build a new certificate authority (CA), run this command and follow the prompts.

    ./easyrsa build-ca nopass

4. Generate the server certificate and key.

    ./easyrsa build-server-full server nopass

5. Generate the client certificate and key. Make sure to save the client certificate and the client private key because you will need them when you configure the client.

    ./easyrsa build-client-full client1.domain.tld nopass

.. note::

    You can optionally repeat this step for each client (end user) that requires a client certificate and key.

6. Copy the server certificate and key and the client certificate and key to a custom folder and then navigate into the custom folder. Before you copy the certificates and keys, create the custom folder by using the mkdir command. The following example creates a custom folder in your home directory.

    mkdir ~/custom_folder/
    cp pki/ca.crt ~/custom_folder/
    cp pki/issued/server.crt ~/custom_folder/
    cp pki/private/server.key ~/custom_folder/
    cp pki/issued/client1.domain.tld.crt ~/custom_folder
    cp pki/private/client1.domain.tld.key ~/custom_folder/
    cd ~/custom_folder/

7. Upload the server certificate and key and the client certificate and key to ACM. Be sure to upload them in the same Region in which you intend to create the Client VPN endpoint. The following commands use the AWS CLI to upload the certificates. To upload the certificates using the ACM console instead, see Import a certificate in the AWS Certificate Manager User Guide. (这一步不是必须的, 你可以选择把文件 download 到本地, 然后再 Console 中进行 Import)

    # 上传 server certificate
    # 注意你的 Cloud9 要有 ACM 对应的 IAM 权限
    aws acm import-certificate --certificate fileb://server.crt --private-key fileb://server.key --certificate-chain fileb://ca.crt

    # 上传 client certificate
    aws acm import-certificate --certificate fileb://client1.domain.tld.crt --private-key fileb://client1.domain.tld.key --certificate-chain fileb://ca.crt

.. note::

    You do not necessarily need to upload the client certificate to ACM. If the server and client certificates have been issued by the same Certificate Authority (CA), you can use the server certificate ARN for both server and client when you create the Client VPN endpoint. In the steps above, the same CA has been used to create both certificates. However, the steps to upload the client certificate are included for completeness.


在 Console 中导入 Server Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果你执行了上一步中的第 7 步, 那么这一步不是必须的.

- Once you have created the certificate, navigate to the AWS Certificate Manager (ACM) console.
- If this is your first time using ACM, click on get started underneath Provision Certificate, then Import a certificate. If you have used ACM before, you should have the option to import a certificate on the dashboard.
- First, import the server certificate. Open the ``ca.crt``, ``server.crt``, and ``server.key`` that you made with easy-rsa in a text editor.
    - Copy and paste the contents of ``server.crt`` into the certificate body field
    - the contents of ``server.key`` into the certificate private key field
    - and the contents of ``ca.crt`` into the certificate chain field. Click Next.
- Optionally, add tags. Click review and import, then import:


配置 VPN Endpoint - 3. 创建 Client VPN Endpoint
------------------------------------------------------------------------------
**创建**

- `进入 VPC 里的 Client VPN Endpoint Console <https://console.aws.amazon.com/vpc/home?#ClientVPNEndpoints:>`_
- 点击 ``Create Client VPN Endpoint``
    - Details:
        - Name Tag = ``sanhe-infra-dev`` 跟你的 VPC 名字一致
        - Client Ipv4 CIDR = ``10.254.0.0/16``. 通常 VPC Ipv4 CIDR 都是 ``x.y.0.0/16`` 一般你的 VPC 的 CIDR block 第一位的数字和这个一样, 第二位写 254, 后面都是 0. 也就是 ``x.254.0.0/16``
    - Authentication Information:
        - Server certificate ARN: 选你刚才上传的 server cert
        - Authentication options: 勾选 Use user-based authentication, 选择 active directory authentication
            - Directory ID: 选你前面配置的 Active Directory 的 ID
    - Other Parameters: **下面的步骤非常重要, 不然你连了 VPN 就上不了公网**.
        - DNS Server 1/2 IP address: 这个填你的 Active Directory 下的两个 DNS name
        - VPC ID: 选你要绑定的 VPC ID
        - Security Group:
            - 选 VPC 里的 Default Security Group. VPN Endpoint 作为连接发起者, 需要跟 VPC 内部的资源通信.
            - 还需要一个 Security Group, 使得能 Allow All traffic from 你的 IP 地址 (ISP 网络服务提供商的地址), 你可以 google My IP 获得这个地址. 并且这个地址有可能会变.
        - 勾选 ``Enable split-tunnel``. 如果不懂什么是 split-tunnel 请看 :ref:`这里 <vpn-split-tunnel>`

**配置**

- `进入 VPC 里的 Client VPN Endpoint Console <https://console.aws.amazon.com/vpc/home?#ClientVPNEndpoints:>`_
- 选定你刚创建的 Client VPN Endpoint:
    - 翻到下面的菜单, ``Target network associations`` -> ``Associate Target Network``, 然后把你的 VPC 里的 public subnet 都选上. 这样你一旦连接了 VPN Endpoint, 就等于你已经在 VPC 的 Public Subnet 上了. 这个 Association 需要等 1-2 分钟才能生效.
    - 翻到下面的菜单, ``Authorization rules`` -> ``Add authorization rule``, 在 ``Destination network to enable access`` 里填你的 VPC Ipv4 CIDR, 这样 Client VPN Endpoint 才能允许来自于 VPC 的 traffic. 在 ``Grant access to:`` 选择 ``Allow access to all users``.
    - 点击 ``Download client configuration``, 这个是登录配置文件, 没有任何敏感信息, 只是方便你用 OpenVPN 软件登录. 下载下来的登录文件最好给他一个名字.


配置 VPN Endpoint - 4. 为 VPC 配置 DHCP
------------------------------------------------------------------------------
创建 DHCP Option:

- 进入 VPC Console -> DHCP Option Sets 菜单 -> 点击 ``Create DHCP Options Set``
- DHCP Options Set Name = 任何名字, 最好和你的 VPC 名字相同, 这样你知道这个是给谁的.
- Domain name = Active Directory 的名字
- Domain name servers = Active Directory 的两个 IP 地址, 用逗号隔开, 中间没有空格.
- 其他用默认, 点击 ``Create DHCP Options Set``

给 VPC 绑定 DHCP Option:

- 进入 VPC Console -> Your VPCs -> 勾选中你的 VPC -> 点击 ``Actions`` -> Edit DHCP Options Set -> 选择你刚刚创建的 VPC


配置 VPN Endpoint - 5. 使用 VPN Client 登录
------------------------------------------------------------------------------
这里我们用 `OpenVPN <https://openvpn.net/vpn-client/>`_ 软件, 用 MacOS 系统登录.

- 下载并安装
- 打开 OpenVPN 软件, 点击左上角的 Files -> Manage Profile -> 导入你之前下载的 client configuration 文件
- 点击链接, 输入 Active Directory 的账号密码, 很快就能看见登录成功了.


总结
------------------------------------------------------------------------------
至此我们成功的将个人电脑连入 VPC 了.


参考资料
------------------------------------------------------------------------------
- https://aws.amazon.com/blogs/storage/accessing-smb-file-shares-remotely-with-amazon-fsx-for-windows-file-server/