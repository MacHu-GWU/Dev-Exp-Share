Use Custom Domain
------------------------------------------------------------------------------

如果你想要用自己的 Domain (http://www.my-website.com) 作为 S3 上的 Static Website 的域名 (原本是 http://example-bucket.s3-website-us-west-1.amazonaws.com), **开启 CORS 是一个很关键的步骤**, CORS 是用于允许 Web Application 或 Mobile Application 上读写取 S3 上的资源. 简单来说, 就是设置一个如果来源是 http://my-website.com 的流量 S3 Bucket 就允许 Read 操作. 然后你在 Domain Registra 服务商那设置了 http://my-website.com, 到你 http://example-bucket.s3-website-us-west-1.amazonaws.com 的映射. 然后从 你的 my-website.com 到 S3 的 Http 请求里就会带上 Origin = my-website.com, 然后你的 S3 就会允许并返回 html 了.

Reference:

- Example: Setting up a Static Website Using a Custom Domain: https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html
- Cross-Origin Resource Sharing (CORS): https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html
- Enable CORS for an API Gateway REST API Resource: https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
- Amazon S3 – Cross Origin Resource Sharing Support: https://aws.amazon.com/blogs/aws/amazon-s3-cross-origin-resource-sharing/
