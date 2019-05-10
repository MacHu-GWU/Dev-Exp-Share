Network
=======

- VPC
- Direct Connect


Note
----

- AWS Site-to-Site VPN 用于将你的数据中心的网络连接到 AWS VPC, AWS Client VPN 用于让具体的用户的电脑连接到 AWS 网络.



Solution
--------

- Q: You have EC2 instances that you need to connect to your on-premises data center. You need to be able to support a connection speed of 200 Mbps. How should you configure this?
- A: Provision a VPN connection between a VPC and data center, Submit a Direct Connect partner request to provision cross-connects between your data center and the Direct Connect location, then cut over from the VPN connection to one or more Direct Connect connections as needed.
- E: VPN and Direct Connect partner request are very important in this

------


- Q: You have been hired as a consultant to provide a solution to integrate a client's on-premises data center to AWS. The customer requires a 300 Mbps dedicated, private connection to their VPC. Which AWS tool do you need?
- A: Direct Connect
- E:
