Congnito
==============================================================================

- User Pool: User pools are user directories that provide sign-up and sign-in options for your app users.
- Identity Pool: Identity pools enable you to grant your users access to other AWS services.
- You can use identity pools and user pools separately or together.


App Authentication Workflow:

1. Authentication and get tokens from User pool
2. Exchange tokens for AWS Credentials
3. Access AWS Service with credentials


Reference:

- What is Amazon Cogonito: https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html


这篇官方文档很好的阐述了 Cognito 的原理以及使用场景. Common Amazon Cognito Scenarios: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-scenarios.html.


这篇文档也很不错的介绍了 Cognito 的用法: https://www.integralist.co.uk/posts/cognito/#client-sdk

6d14ca5b-ea45-4001-ac50-557b558ec4f6

学习 Cognito 的时候, 你首先需要对 身份验证, 授权 以及相关的 Oauth2 和 OIDC (OpenId Connect) 有一定的了解. 这几篇文章含金量非常高.

- 基于OAuth2的认证（译）: https://www.cnblogs.com/linianhui/p/authentication-based-on-oauth2.html
- Json Web TOken: https://www.cnblogs.com/linianhui/p/oauth2-extensions-protocol-and-json-web-token.html#auto_id_5
- OIDC（OpenId Connect）身份认证（核心部分）: https://www.cnblogs.com/linianhui/archive/2017/05/30/openid-connect-core.html