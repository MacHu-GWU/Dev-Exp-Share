

Client -- 1 --> API Gateway Http Server -- 2 --> Integrated Computation System (Lambda, Http Server, EC2, ECS ...) -- 3 --> API Gateway Http Server -- 4 --> Client

1. Method Request

决定了你发起请求时请求标准. 比如允许哪些 Parameters, 是否必须要求这些 Parameters, 允许哪些哪些 Headers, 是否必须要求这些 Headers.

URL Query String Parameters

2. Integration Request

定义了 API Gateway 和具体实现方式之间如何集成. 例如 Lambda 只能接受 JSON 输入输出, 那么你将 Endpoint, Parameters, Headers, Payload 发送给 Api Gateway 之后, 需要将这些信息汇总, 打包放入 JSON 传给 Lambda. 那么这个打包过程就在 Integration Request 中定义.

3. Integration Response



4.