How can I grant internet access to my VPC Lambda function?
==============================================================================

Reference: https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/


Issue
------------------------------------------------------------------------------
I want to give my VPC-enabled AWS Lambda function internet access. How can I do this?


Short Description
------------------------------------------------------------------------------
If your Lambda function needs to access private VPC resources (for example, an Amazon RDS DB instance or Amazon EC2 instance), you must associate the function with a VPC. If your function also requires internet access (for example, to reach a public AWS service endpoint), your function must use a NAT gateway or instance. For more information, see VPC Endpoints.

To add a VPC configuration to your Lambda function, you must associate it with at least one subnet. If the function needs internet access, you need to follow two rules:

- The function should only be associated with private subnets.
- Your VPC should contain a NAT gateway or instance in a public subnet.

**Whether a subnet is public or private depends on its route table**. Every route table has a default route, which determines the next hop for packets that have a public destination.

- **Private subnet**: the default route points to a NAT gateway (nat-...) or NAT instance (eni-...).
- **Public subnet**: the default route points to an internet gateway (igw-...).

If your VPC already has a public subnet (with a NAT) and one or more private subnets for your Lambda function, then you only need to follow the steps in “Configure your function".


Resolution
------------------------------------------------------------------------------
**Configure your function**

Identify your private and public subnets:

1. In the VPC console, from the navigation pane, choose **Subnets**.
2. Select a subnet, and then choose the Route Table tab. Verify the default route:
    - **Public subnet**: Destination: 0.0.0.0/0, Target: igw-…
    - **Private subnet**: Destination: 0.0.0.0/0, Target: nat-… or eni-…

Associate the function with private subnets:

1. In the Lambda console, choose your function, and then choose **Configuration**.
2. Expand **Advanced settings**, expand **VPC**, and then choose your VPC.
3. Expand **Subnets** and choose only private subnets.
4. Expand **Security Groups**, choose a security group, and then choose **Save**.

**To create a public or private subnet**

In the VPC console, from the navigation pane, choose Subnets.
To create a new subnet, choose Create Subnet. Otherwise, choose an existing subnet.
Choose the Route Table tab, and then choose Edit.
From the Change to: drop-down menu, choose an appropriate route table:
For a private subnet, the default route should point to a NAT gateway or NAT instance:

.. code-block:: bash

    Destination: 0.0.0.0/0
    Target: nat-… (or eni-…)

For a public subnet, the default route should point to an internet gateway:

.. code-block:: bash

    Destination: 0.0.0.0/0
    Target: igw-…

**To create a route table for a public or private subnet**

1. In the VPC console, choose Route Tables, and then choose Create Route Table.
2. In the Name tag field, enter a name that is meaningful to you, select the VPC drop-down menu and choose your VPC, and then choose Yes, Create.
3. Select the new route table, and then choose the Routes tab.
4. Choose Edit, and then choose Add another route.

Destination: 0.0.0.0/0

Target:

- For a private subnet with a NAT instance: eni-…
- For a private subnet with a NAT gateway: nat-…
- For a public subnet: igw-…

**To create an internet gateway**

1. In the VPC console, from the navigation pane, choose **Internet Gateways**, and then choose **Create Internet Gateway**.
2. In the **Name tag** field, enter a name and then choose **Yes, Create**.
3. Select the internet gateway, and then choose **Attach to VPC**.

**To create a NAT gateway**

1. In the VPC console, from the navigation pane, choose **NAT Gateways**, and then choose **Create NAT Gateway**.
2. In the **Subnet** field, choose a public subnet.
3. In the **Elastic IP Allocation ID** field, choose an existing Elastic IP address, or select **Create New EIP**, and then choose **Create a NAT Gateway**.


允许位于 VPC 上的 Lambda 访问公网
==============================================================================

逻辑上决定一个 Subnet 是公网还是私网的是 Route Table, Route Table 只为 Outbound Traffic 服务. 管理 Inbound Traffic 是 Security Group 和 Network ACLs.

- Private Subnet: 通往 VPC IP 以外的流量导向 NAT Gateway / Instance
- Public Subnet: 通往 VPC IP 以外的流量导向 Internet Gateway

通往 VPC IP 的流量导向 Local, 也就是 VPC 本身.


Route Table
------------------------------------------------------------------------------

- 对于 1 个 VPC 只能有一个 Main Route Table. 通常这个 Main Route Table 是为 Private Subnet 服务的. 也就是将所有流量导向 NAT Gateway
- 所有没有定义 Route Table 的 Subnet 都会默认继承 Main Route Table 的设置 (非 Main Route Table 的设置不会被继承).
- 对于 Public Subnet, 需要设置 Route Table, 将流量导向 Internet Gateway.


Security Group
------------------------------------------------------------------------------

- Lambda 所在的 Security Group 要允许和 Outbound