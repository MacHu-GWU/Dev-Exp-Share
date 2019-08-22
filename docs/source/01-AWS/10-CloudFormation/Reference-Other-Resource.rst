引用其他 AWS Resource
==============================================================================

我们来假设一个应用场景, 我们设计了一个 Cloudformation Template, 里面包含了许多 Api Gateway, Api Resource, Api Method, Lambda Function, Lambda Permission 的 Serverless 应用. 而我们可以为这个 Serverless 自己创建一个 ApiGW RestApi, 也可以引用别人的 ApiGW RestApi, 这是因为我们的这个 Api 上可能还有不是用 Lambda 实现的 API, 那我们在我们的 Cloudformation Template 中要如何设定呢?

首先, 我们要知道, Api Resource 需要引用 ApiGW RestApi 的 Id 以及它的 RootResourceId. 而我们有两种方式

1. 直接在我们的 CF Template 中定义一个 ``AWS::ApiGateway::RestApi``, 然后引用它的 logic id, 这是作为开发测试使用的, 到生产环境中需要引用别人的 ApiGW RestApi.
2. 为 CF Template 加 2 个 Parameter, 分别对应 RestApi Id 和 RootResourceId, 然后使用 ``{"Ref": "<ParameterLogicId>"}`` 引用.

显然开发模式 1 并不是一个号的选择, 因为开发环境和生产环境的代码不一致, 无法方便的在两者之间切换. 而方法 2 就很科学了. 作为调试, 你可以自己手动使用 CloudFormation 创建一个 ApiGW RestApi, 然后创建两个 Output, 并给予 Export Name, 然后再在你的 ApiGW Stack