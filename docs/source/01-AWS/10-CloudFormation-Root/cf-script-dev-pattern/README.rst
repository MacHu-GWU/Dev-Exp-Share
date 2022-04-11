一个简单, 却又包含了大部分设计模式的 CloudFormation 项目
==============================================================================

.. contents::
    :local:


案例分析
------------------------------------------------------------------------------

假设我们要创建一个 **微服务, 将 Web 服务器上传到某个已存在的 Bucket 中的 CSV 文件转化成 Parquet 并储存到另一个 Bucket 中**. 整个服务要用到的 AWS Resource 有:

1. 创建一个 Bucket, 称之为 destination-bucket.
2. 创建一个 IAM Role, 用于执行 Lambda.
3. 创建一个 Lambda Function, 监听 origin-bucket 中的 put object 事件. 执行转换后写入到 destination-bucket 中.

service name 就叫做 ``my-service`` 好了, stage 我们使用 ``dev`` 好了.


设计模式
------------------------------------------------------------------------------

CloudFormation Template 由于细节很多, 如果你有 10 个以上的资源, 你的 template 很容易就超过 500 行, 所以一个更好的做法是 **将 Resource 分为各个子模块** (英文叫做 Tier), 放在不同的 template 中, 这些子模块叫做 **nested stack**. **原则上各个 nested stack 互相之间应该没有依赖关系**.

最后在一个 master template 中用一个特殊的 Resource ``AWS::CloudFormation::Stack`` 引用这些 nested stack, 然后利用 ``Outputs`` 引用在这些 nested stack 中, 动态生成的变量. 在 master template 中定义剩下的 Resource 即可.

所有的 master stack 和 nested stack 共用一批 parameters.


代码解析
------------------------------------------------------------------------------

在本例中:

- ``my-service-s3-tier.json``: nested stack1, 最先被创建.
- ``my-service-iam-role-tier.json``: nested stack2, 第二个被创建, master stack 中的 lambda 需要用到其中的 iam role.
- ``my-service.json``: master stack, 最后被创建.
- ``config.json``: 所有 stack 需要用到的 parameters.
- ``deploy.sh``: 应用整个 stack 的脚本.

**parameters 的引用和传递顺序**:

nested stack ``my-service-s3-tier.json`` 需要依赖一堆参数.

.. code-block:: python

    # content of my-service-s3-tier.json
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Metadata": {},
        "Parameters": {
            "ServiceName": {
                "Type": "String",
                "Description": "Specify your service name."
            },
            "Stage": {
                "Type": "String",
                "Description": "Specify your stage."
            },
            "StackName": {
                "Type": "String",
                "Description": "The main stack name."
            },
            "AWSAccountAlias": {
                "Type": "String",
                "Description": "Specify your stage."
            },
            "ResourceNamePrefix": {
                "Type": "String",
                "Description": "A prefix used in all aws resource name as prefix."
            },
            "S3BucketPrefix": {
                "Type": "String",
                "Description": "A prefix used for s3 bucket used by this stack, since s3 is a global service, the aws account alias is appended left."
            }
        },
        "Resources": {
            "DestinationBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": {
                        "Fn::Sub": [
                            "${S3BucketPrefix}-destination",
                            {
                                "S3BucketPrefix": {
                                    "Ref": "S3BucketPrefix"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }


master stack ``my-service.json`` 是这样引用 ``my-service-s3-tier.json`` 的. 请注意, 由于 ``my-service-s3-tier.json`` 本身就依赖一些 parameters. 而你在使用 master stack 的时候, 是给 master stack 直接传递参数的, **而 nested stack 则必须要显示地将传递给 master stack 的参数, 转送给 nested stack**.

.. code-block:: python

    "S3Tier": {
        "Type": "AWS::CloudFormation::Stack",
        "Properties": {
            "TemplateURL": "./my-service-s3-tier.json",
            "Parameters": {
                "ServiceName": {
                    "Ref": "ServiceName"
                },
                "Stage": {
                    "Ref": "Stage"
                },
                "StackName": {
                    "Ref": "StackName"
                },
                "AWSAccountAlias": {
                    "Ref": "AWSAccountAlias"
                },
                "ResourceNamePrefix": {
                    "Ref": "ResourceNamePrefix"
                },
                "S3BucketPrefix": {
                    "Ref": "S3BucketPrefix"
                }
            }
        }
    },

注意的是, **一个 template 中被声明过的 parameters 必须要有值, 如果你从 command line 中传递进去的值不够, 则会报错. 但你从 command line 如果传入了过多的值, 却不会有问题**.


**在 master stack 中引用 nested stack 的 Outputs**:

观察 nested stack ``my-service-iam-role-tier.json``, 这里 **显示地定义了** ``Outputs.LambdaExcutionRoleARN`` 这一变量.

.. code-block:: python

    "Outputs": {
        "LambdaExcutionRoleARN": {
            "Description": "",
            "Value": {
                "Fn::GetAtt": [
                    "LambdaExcutionRole",
                    "Arn"
                ]
            }
        }
    }

观察 master stack ``my-service.json``, 这里我们用 GetAtt 函数, 从 ``IamRoleTier`` 中获取了之前定义的 ``LambdaExcutionRoleARN``,

.. code-block:: python

    "TheLambdaFunction": {
        "Type": "AWS::Lambda::Function",
        "Properties": {
            ...
            "Role": {
                "Fn::GetAtt": [
                    "IamRoleTier",
                    "Outputs.LambdaExcutionRoleARN"
                ]
            }
        }
        ...
    }


开发技巧
------------------------------------------------------------------------------

**技巧 1: 单独调试每一个 nested stack, 尝试用 create-stack 单独创建每个 nested stack**

请观察 ``my-service-s3-tier.json`` 的代码, 由于这是一个 nested stack, 且不依赖任何其他的 stack, 当然你可以将其直接放到 cloudformation 中, 或用 ``aws cloudformation create-stack ...`` 创建. 如果单独创建失败, 那么最终 master stack 肯定也会失败. 调试一个小文件肯定要容易一些.

**技巧 2: 单独调试每一个 resource, 尝试用 create-stack 单独创建每个 resource**

这里我们有两个脚本 ``test.py``, ``test.json`` 和 ``helper.py``. 在 ``test.json`` 中, 我们定义了一个只有一个 resource 的 stack, 为了方便起见, 里面不需要任何 parameters. ``test.py`` 用于创建这个 stack, 而 ``helper.py`` 用于在你手动创建 resource 之后, 调用 boto3 api 查看 resoure 背后的数据. 你可以将手动创建的 resource 背后的数据, 与你用 cloudformation 创建的 resource 背后的数据进行比对, 再结合 cloudformation 文档你就知道你还缺什么了.

**技巧 3 用 shell script 和 aws cli 完成 deploy**

如果你使用 nested stack, 那么常规的 upload template 的方法就不管用了, 因为只 upload master stack template 是没用的. aws cli 提供了 ``aws cloudformation pacakge`` 命令, 用于合并你所有的 template. ``aws cloudformation deploy`` 命令则将 master stack 一次部署.

这里要注意, ``deploy`` 命令不支持从 json 文件中读取参数, 所以我写了 ``convert_parameters.py`` 脚本, 用于将 json 数据转化成 ``deploy`` 命令所能接受的格式.

**特别注意! parameters 的变量名只允许大小写英文, 变量值不允许空格, 只允许下划线和横杠**


从删库到跑路
------------------------------------------------------------------------------
CloudFormation 中使用 ``Delete Stack`` **要特别注意**. 因为你一旦 Delete Stack, 那么 AWS Resource 上的数据也会一并删除.


Reference:

- Working with Nested Stacks: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html