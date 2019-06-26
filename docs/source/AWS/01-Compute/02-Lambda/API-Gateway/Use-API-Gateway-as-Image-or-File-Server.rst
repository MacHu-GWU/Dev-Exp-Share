Use API Gateway as Image or File Server
==============================================================================

Reference:

- Create a REST API as an Amazon S3 Proxy in API Gateway: https://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html

这篇文档信息量很大, 但是他不说人话!

首先我们来思考一下 文件服务器 应该是怎么样的?


API Gateway + S3 实现文件服务器
------------------------------------------------------------------------------

- POST api.example.com/my-bucket/filename.txt
- GET api.example.com/my-bucket/filename.txt
- DELETE api.example.com/my-bucket/filename.txt

FAQ
------------------------------------------------------------------------------

为什么我们不用 Lambda. Lambda 的 Request Payload 有 6MB 的限制, 你无法上传大文件.
