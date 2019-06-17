Elastic Map Reduce (EMR)
==============================================================================

EMR 是对 Hadoop, HDFS, Hive 的一个封装, 让用户无需管理 Hadoop 所需要的资源, 而专注于实现业务逻辑.

Hadoop 的相关概念:

1. Hadoop: 一种 Map Reduce 的编程模型,
2. HDFS: Hadoop File System, Hadoop 集群
3. HIVE: Hadoop Data warehouse software, 用抽象数据集语言定义类 SQL 的数据表, 然后用集群执行 Query 进行分析.


EMR Concept
------------------------------------------------------------------------------

- Cluster: 多个 EC2 实例组成的集群
    - Long-Running Cluster: 在 Console 里叫做 Cluster Execution, 启动后不关机.
    - Transient Cluster: 在 Console 里叫做 Step execution, scheduled work, cron job.
Transient vs Long-running cluster. 每次任务完成后关闭所有实例. 每次启动时要一段时间为 EC2 安装软件.
- Node:
    - Leader Node (**Master Node**)
        - Manages the Cluster by coodinating the distribution of data and task
        - Track status of tasks
        - Every cluster has leader node
    - Work Node (**Slave Node**)
        - Core Node
            - store data in the HDFS of the cluster
            - multi-node clusters have at least one work node
        - Task Node (Compute Node), 通常使用 Spot Instance
            - does not store data


EMR Cluster Lifecycle
------------------------------------------------------------------------------

- Starting
- Bootstraping
    - run any boostrapping actions
    - install custom applications
    - perform customizations
- EMR installing the native applications:
    - Hive, Spark, Hadoop ...
- Running
- Waiting
- Shutting Down
- Completed


Access EMR Cluster
------------------------------------------------------------------------------

Accessing a Cluster

1. IAM
2. Kerberos: Kerberos is a computer network authentication protocol that works on the basis of tickets to allow nodes communicating over a non-secure network to prove their identity to one another in a secure manner.
3. SSH

EMR IAM roles:

- You can customize and restrict the permissions on an EMR cluster in order secure your data
- Be default, EMRFS uses the IAM role attached to the cluster to access to S3
- EMR can be configured with a role that allows it to automatically scale to meet demand



EMR Architect
------------------------------------------------------------------------------


Storage:
    - Hadoop Distributed File System (HDFS):
    - EMR File System (EMRFS): 其实就是使用 S3 作为 File System, 主要用来保存 input, ouput, intermediate results
    - Local File System

Cluster Resource Management
    - YARN (Yet Another Resource Negotiator)
Data Processing Framework
    - Hadoop Reduce
    - Apache Spark
Applications and Programs
    - Hive: data warehouse software, Data Define Language.
    - Pig: Apache Pig is a high-level platform for creating programs that run on Apache Hadoop. The language for this platform is called Pig Latin. Pig can execute its Hadoop jobs in MapReduce, Apache Tez, or Apache Spark.
    - Spark Streaming Library:



