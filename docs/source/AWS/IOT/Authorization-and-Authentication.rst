Authorization and Authentication
==============================================================================

1. IOT Device: X.509 Certification
2. Mobile Application: AWS Cognito
3. Web / Desktop Application: IAM or Federate Identities.


2, 3 都比较好理解, 我们重点来说一下 1.

1 实际上是在 AWS Console 里注册一个 Certification, 然后将 IOT API 的操作权限 Attach 给一个 Policy. 在 IOT 的硬件中, 将 Public Key 和 Private Key 写入硬件, 然后硬件



IOT Message Broker
==============================================================================

- Publisher
- Topic
- Subscriber