Use IAM Role or Instance Profile in EC2
==============================================================================

在个人电脑上开发时, 通常用的是 IAM User 的 Access Key. 而在 EC2 机器上, 为每一台机器配置一个 IAM User, 并且同步密码是不显示, 且非常不安全的. 最好的方法是为机器创建一个 IAM Instance Profile, 一个类似于 IAM Role 的东西, 只不过用户是一个虚拟机而已.

- Using an IAM Role to Grant Permissions to Applications Running on Amazon EC2 Instances: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html
- Use CloudFormation configure EC2 Iam Instance Profile: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-iaminstanceprofile
