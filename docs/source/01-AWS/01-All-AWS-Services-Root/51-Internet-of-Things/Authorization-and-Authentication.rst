Authorization and Authentication
==============================================================================

Ref:

- AWS IoT Authentication: https://docs.aws.amazon.com/iot/latest/developerguide/iot-authentication.html

AWS IOT 支持 4 种验证方式:

- X.509 certificates
- IAM users, groups, and roles
- Amazon Cognito identities
- Federated identities

1. IOT Device: 用 X.509 Certification
2. Mobile Application: 用 AWS Cognito
3. Web / Desktop Application: 用 IAM or Federate Identities.

2, 3 都比较好理解, 我们重点来说一下 1.

1 实际上是在 AWS Console 里注册一个 Certification, 然后将 IOT API 的操作权限 Attach 给一个 Policy. 在 IOT 的硬件中, 将 Public Key 和 Private Key 写入硬件, 然后硬件就可以用这个 Certification. 这跟 Https 的 Certification 类似. 只不过 Https 的证书由多家可信的大公司发布, 而这里是由 AWS 发布.


IOT Message Broker
==============================================================================

- Publisher
- Topic
- Subscriber