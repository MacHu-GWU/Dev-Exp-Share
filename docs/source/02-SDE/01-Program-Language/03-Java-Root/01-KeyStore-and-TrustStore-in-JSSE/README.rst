.. _java-keystore-and-truststore-in-jsse:

KeyStore and TrustStore in JSSE
==============================================================================
本文原文位于: https://blog.csdn.net/andy_zhang2007/article/details/78805578

在 Java 中有一个内置库 JSSE (Java Secure Socket Extension), 实现了各种 Authentication 协议. Keystore 和 Truststore 是 JSSE 中的两种文件, 这两种文件都使用 Java 的 keytool 来管理.

比如在客户端 (服务请求方) 对服务器 (服务提供方) 发起一次 HTTPS 请求时, 服务器需要向客户端提供认证以便客户端确认这个服务器是否可信. 这里, 服务器向客户端提供的认证信息就是自身的证书和公钥, 而这些信息, 包括对应的私钥, 服务器就是通过 KeyStore 来保存的. 当服务器提供的证书和公钥到了客户端, 客户端就要生成一个TrustStore 文件保存这些来自服务器证书和公钥.

**TrustStore 是用于客户端认证服务器是否可信. 而 KeyStore 是用于服务器认证客户端的**.

KeyStore 和 TrustStore的不同, 也主要是通过上面所描述的使用目的的不同来区分的, 在 Java 中这两种文件都可以通过 keytool 来完成. 不过因为其保存的信息的敏感度不同, KeyStore 文件通常需要密码保护.

正是因为 KeyStore 和 TrustStore Java 中都可以通过 keytool 来管理的, 所以在使用时多有混淆. 记住以下几点, 可以最大限度避免这些混淆:

- 如果要保存你自己的密码, 秘钥和证书, 应该使用 KeyStore, 并且该文件要保持私密不外泄, 不要传播该文件
- 如果要保存你信任的来自他人的公钥和证书, 应该使用 TrustStore, 而不是 KeyStore

在以上两种情况中的文件命名要尽量提示其安全敏感程度而不是有歧义或者误导. 拿到任何一个这样的文件时, 确认清楚其内容然后决定怎样使用.

因为 KeyStore 文件既可以存储敏感信息, 比如密码和私钥, 也可以存储公开信息比如公钥, 证书之类, 所有实际上来讲, 可以将 KeyStore 文件同样用做 TrustStore 文件, 但这样做要确保使用者很明确自己永远不会将该 KeyStore 误当作 TrustStore 传播出去.
