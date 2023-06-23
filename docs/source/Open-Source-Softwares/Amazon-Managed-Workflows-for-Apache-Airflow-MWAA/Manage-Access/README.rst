Manage Access

- Accessing an Amazon MWAA environment: 这个权限是给登录 AWS MWAA Console 或用 API 来管理 MWAA cluster 用的.
- Service-linked role for Amazon MWAA: 这个权限是给 AWS MWAA 这个 Service 用的, 让它能调用其他的 Service 的 API, 这个不是给 Cluster 用的.
- Amazon MWAA execution role: 这个是给 Executor 执行编排的时候用的. 这里主要有 4 个权限是必须的:
    - 访问 AWS CloudWatch 写日志的权限
    - 访问用来储存 DAG 的 S3 Bucket 的权限
    - 访问用来储存调度任务的 SQS 的权限
    - 访问 KMS 用来加密解密数据的权限
- Cross-service confused deputy prevention: 这个就是防止越权
- Apache Airflow access modes: 这个是 Airflow 软件本身提供的访问模型, 这里主要说的是网络模型