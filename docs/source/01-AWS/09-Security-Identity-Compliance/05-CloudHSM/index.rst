AWS CloudHSM
==============================================================================

**什么是 HSM (Hardware Security Module)**:

是一种硬件设备专门用于加密, 内置了硬件实现的加密算法, 高强度, 高性能.

**什么是 CloudHSM**:

AWS CloudHSM is a cloud-based hardware security module (HSM) that enables you to easily generate and use your own encryption keys on the AWS Cloud.

简单来说, 就是你自己生成秘钥, 放在 CloudHSM 上保管, 用户对秘钥完全可控, 可见. KMS 常用的两种秘钥保管策略是:

1. 用 AWS 管理的秘钥. AWS 会为每个 AWS Account 生成一批对用户不可见的秘钥.
2. 用户生成的秘钥, 用户可以控制秘钥的生成, 过期, 删除, 但是无法看到具体的秘钥.

第三种策略就是使用 CloudHSM 了.
