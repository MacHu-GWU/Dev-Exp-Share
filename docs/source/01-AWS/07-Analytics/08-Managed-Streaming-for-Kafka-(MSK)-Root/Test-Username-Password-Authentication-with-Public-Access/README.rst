https://docs.aws.amazon.com/msk/latest/developerguide/public-access.html

为了启用 Public Access, 你需要启用这些:

To turn on public access to a cluster, first ensure that the cluster meets all of the following conditions:

- The subnets that are associated with the cluster must be public. This means that the subnets must have an associated route table with an internet gateway attached. For information about how to create and attach an internet gateway, see Internet gateways in the Amazon VPC user guide.
- MSK 所在的 Subnet 必须要是 Public Subnet.
- Unauthenticated access control must be off and at least one of the following access-control methods must be on: SASL/IAM, SASL/SCRAM, mTLS. For information about how to update the access-control method of a cluster, see Updating a cluster's security settings.
- ``Unauthenticated access control`` 这个选项必须关闭. 必须启用 ``SASL/IAM, SASL/SCRAM, mTLS`` 其中至少一种鉴权方式. 具体方式是在 Console 里点 Action -> Edit Security Settings
- Encryption within the cluster must be turned on. The on setting is the default when creating a cluster. It's not possible to turn on encryption within the cluster for a cluster that was created with it turned off. It is therefore not possible to turn on public access for a cluster that was created with encryption within the cluster turned off.
- 在 Cluster 内部使用 TSL 加密必须要启用. 由于如果你启用 MSK Cluster 的时候如果禁用了 Cluster 内部 TSL 加密, 那么你之后是无法启用的, 也就是说你永远无法启用 Public Access. 总结就是你必须启用 MSK 的时候就启用在 Cluster 内部使用 TSL 加密.
- Plaintext traffic between brokers and clients must be off. For information about how to turn it off if it's on, see Updating a cluster's security settings.
- 默认情况下 Client 到 Broker 的连接是开启了 TSL 加密的, Plaintext 是默认关闭的.
- If you are using the SASL/SCRAM or mTLS access-control methods, you must set Apache Kafka ACLs for your cluster. After you set the Apache Kafka ACLs for your cluster, update the cluster's configuration to have the property allow.everyone.if.no.acl.found to false for the cluster. For information about how to update the configuration of a cluster, see Amazon MSK Configuration Operations. If you are using IAM access control and want to apply authorization policies or update your authorization policies, see IAM access control. For information about Apache Kafka ACLs, see Apache Kafka ACLs.