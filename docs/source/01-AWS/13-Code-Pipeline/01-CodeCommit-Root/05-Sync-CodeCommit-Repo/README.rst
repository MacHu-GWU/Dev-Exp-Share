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

我个人更喜欢第一个方法, 因为我对价格更加敏感. 下面我来介绍一下我的详细方案.

**Backup account setup**

也就是用来存放备份的 AWS Account 的设置. 首先你要创建一个 S3 Bucket. 然后你要给这个 S3 Bucket 创建一个 bucket policy, 用来允许 CodeBuild 来 push 文件到这个 bucket. 这个 policy 的内容如下.

.. literalinclude:: ./backup_account_bucket_policy.json
   :language: python

- 你需要将 ``${codecommit_aws_account_id}`` 替换成 codecommit repo 所在的 AWS Account ID
- 以及 ``${backup_bucket}`` 替换成这个 S3 Bucket name
- 然后 ``${backup_folder}`` 我推荐用 ``projects/codecommit-backup/${codecommit_aws_account_id}/*``. 而最终的备份文件的路径则是: ``projects/codecommit-backup/${codecommit_aws_account_id}/${codecommit_aws_region}/${repo_name}/${repo_name}-${datetime}.zip``.

这个 Policy 的好处是, 很可能你这个 CodeCommit account 上的 repo 在不同的 region, 你无需修改这个 policy 就能从多个 region 备份.

**CodeCommit account setup**

也就是 CodeCommit repo 所在的 AWS Account 的设置. 首先你要创建一个 IAM Role 给 CodeBuild 用. 这个 Role 需要能创建 CloudWatch log group (因为要打 log 上去), 能对 backup bucket 进行基本的操作, 以及能从 codecommit 上 pull 代码. 由于 IAM Role 是 global 的, 而 CodeBuild 是 regional 的, 所以这个 IAM Policy 里的 region 信息都是用的 ``*``.

.. literalinclude:: ./codebuild_iam_policy.json
   :language: python

- 你需要将 ``${codecommit_aws_account_id}`` 替换成 codecommit account id.
- ``${codebuild_project_name}`` 替换成你这个 CodeBuild project 的名字, 我推荐就用 ``codecommit-backup`` 并在所有的 region 保持一致.
- ``${backup_bucket}`` 和 ``${backup_folder}`` 与前面说的保持一致.

Reference:

- Automate event-driven backups from CodeCommit to Amazon S3 using CodeBuild and CloudWatch Events: https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-event-driven-backups-from-codecommit-to-amazon-s3-using-codebuild-and-cloudwatch-events.html
