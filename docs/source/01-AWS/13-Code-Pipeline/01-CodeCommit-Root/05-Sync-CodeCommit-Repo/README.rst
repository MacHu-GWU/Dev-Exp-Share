Sync CodeCommit Repo
==============================================================================
Keywords: AWS CodeCommit Repository, Repo, Git, Backup


Summary
------------------------------------------------------------------------------
Git repo 是一个公司最宝贵的资源之一 (另一个是 data), 凝聚了工程师花费了很多时间的开发工作. 如果一个 repo 消失了, 那么这么多时间都白费了. 所以为 repo 创建一个 backup 是非常非常重要的. 除此之外, 有时候还会有 fork 一个 repo 到另一个 repo 的需求, 这就跟 github 上的 fork 功能类似了. 但是你不要想进行双向同步, 因为这是在逻辑上不成立的, 必然会破坏代码库的稳定. 以上两种情况可以用同一个办法解决. 下面我们就来介绍这种方法.


Solution
------------------------------------------------------------------------------
简单来说, 就是将代码库全部历史 git clone 下来, 然后 zip 打包, 放到 S3 上 (cross account 也没问题). 这个工作可以放在 CodeBuild 里去做. 然后具体从哪个 Repo 的哪个 Reference 上 pull 则用 CodeBuild 的 environment variable 来控制. 下面这是一个 CodeBuild 的 buildspec.yml 的例子:

.. code-block:: yaml

    version: 0.2
    phases:
      install:
        commands:
          - pip install git-remote-codecommit
      build:
        commands:
          - env
          - git clone -b $REFERENCE_NAME codecommit::$REPO_REGION://$REPOSITORY_NAME
          - dt=$(date '+%d-%m-%Y-%H:%M:%S');
          - echo "$dt"
          - zip -yr $dt-$REPOSITORY_NAME-backup.zip ./
          - aws s3 cp $dt-$REPOSITORY_NAME-backup.zip s3:// #substitute a valid S3 Bucket Name here


Enterprise Read Solution
------------------------------------------------------------------------------
在企业中, 通常所有的 repo 都会放在同一个 AWS Account 和 Region 上, 而且要备份的 repo 数量会很多. 这时候为每个 repo 创建一个 CodeBuild project 就不合适了, 我们应该用一个 CodeBuild 来搞定所有的 CodeCommit. 我们可以用两种方式实现:

1. 用一个运行时间较长的 build run, 然后用一个 for loop 来搞定. 这样的坏处是前面的 build 可能会让后面的 build fail, 好处是实现简单, 总体开销比 batch 低.
2. 用 Batch build. 这样的坏处是每一个 sub build 都有 provision 阶段, 等于这段时间的开销翻了好多倍. 好处是编排管理更自动化, 同时运行一次的时间更快.

我个人更喜欢第一个方法, 因为我对价格更加敏感.

我具体的设置如下:

Backup account


.. literalinclude:: ./backup_account_bucket_policy.json
   :language: python


Reference:

- Automate event-driven backups from CodeCommit to Amazon S3 using CodeBuild and CloudWatch Events: https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-event-driven-backups-from-codecommit-to-amazon-s3-using-codebuild-and-cloudwatch-events.html
