.. _aws-ecr:

Elastic Container Registry
==============================================================================

相当于私有的 DockerHub 服务, 用于注册, 管理你的 Docker Image.


https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html


docker build -t my-web-app:1 .

docker tag e9ae3c220b23 aws_account_id.dkr.ecr.region.amazonaws.com/my-web-app

docker push 110330507156.dkr.ecr.region.amazonaws.com/my-web-app


110330507156.dkr.ecr.us-east-1.amazonaws.com/aws-ls-docker