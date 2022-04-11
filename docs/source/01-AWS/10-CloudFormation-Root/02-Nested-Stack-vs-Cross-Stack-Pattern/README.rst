Nested Stack vs Cross Stack Pattern
==============================================================================

由于 AWS Resource 很多 Property 也很多, CloudFormation 很容易变得很大. 在程序设计上, 维护一个大文件永远是不容易做到而且容易出错的.

更好的做法是 尽可能的将互相独立的 AWS Resource 分离开, 放在不同的 Stack 上. CloudFormation 有两种主要的设计模式可以实现这一点, Nested Stack 模式和 Cross Stack Reference 模式.


Nested Stack 模式
------------------------------------------------------------------------------

每 1 个 Template 文件通常对应着 1 个 Stack. 但是你可以将多个 Stack Nest 在一个 Master Stack 中, 最终你只用 Deploy Master Stack,

根据 Master Stack 对其他 Template 引用的顺序和 DependsOn 的设置, 会自动按顺序先 Deploy Child Stack 最后再 Deploy Master Stack 中的 Resource.

参数传递的顺序是, 先从命令行通过 Parameters 传给 Master Stack, 然后 Master Stack 中的 Nested Stack 被定义为 Resource, 其中有一个 Properties 为 Parameters, 用于将全局参数传递给 Nested Stack.

VPC Stack, EnvironmentName 为必选参数, 01-vpc-tier.json:

.. code-block:: javascript

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {
            "EnvironmentName": {
                "Type": "String",
                "Description": "An environment name that will be prefixed to resource names"
            }
        },
        "Resources": {
            "VPC": {
                "Type": "AWS::EC2::VPC",
                "Properties": {
                    ...
                }
            }
        }
    }

Master Stack, 有很多其他参数, 99-master.json:

.. code-block:: javascript

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Parameters": {
            "EnvironmentName": {
                "Type": "String",
                "Description": "An environment name that will be prefixed to resource names"
            },
            ... master stack may have more parameters
        }
        "Resources": {
            "VPCTier": {
                "Type": "AWS::CloudFormation::Stack",
                "Properties": {
                    "TemplateURL": "./01-vpc-tier.json",
                    "Parameters": {
                        "EnvironmentName": {
                            "Ref": "EnvironmentName"
                        }
                    }
                }
            },
            ... master stack may have more resources
        }
    }


Cross Reference 模式
------------------------------------------------------------------------------

在这种模式中, 多个 Stack 之间的 Dependence 和 先后顺序是由开发者自己管理的. 这个 Export Name 的引用是全局有效的, 也就是说整个 AWS Account 下的 Stack2 要想读取 Stack1 里的 ExportName, 无需知道 Stack1 的名字, 只要 ExportName 对就 OK. 所以这个 ExportName 最好要使用 StackName 或 EnvironmentName 作为前缀.

Stack1, 先被部署, ``BucketNameInExport`` 是 Exported Output::

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "S3Bucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "AccessControl": "Private",
                    "BucketName": "my-bucket-name-1",
                    "PublicAccessBlockConfiguration": {
                        "BlockPublicAcls": true,
                        "BlockPublicPolicy": true,
                        "IgnorePublicAcls": true,
                        "RestrictPublicBuckets": true
                    }
                }
            }
        },
        "Outputs": {
            "BucketName": {
                "Value": {
                    "Ref": "S3Bucket"
                },
                "Export": { "Name" : "BucketNameInExport"}
            }
        }
    }

Stack2, 使用 "Fn::ImportValue" 导入 ``BucketNameInExport``::

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "S3Bucket1": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "AccessControl": "Private",
                    "BucketName": {
                        "Fn::Sub": [
                            "${Name}-replica",
                            {
                                "Name": {"Fn::ImportValue" : "BucketNameInExport"}
                            }
                        ]
                    },
                    "PublicAccessBlockConfiguration": {
                        "BlockPublicAcls": true,
                        "BlockPublicPolicy": true,
                        "IgnorePublicAcls": true,
                        "RestrictPublicBuckets": true
                    }
                }
            }
        }
    }


两种模式该如何选择?
------------------------------------------------------------------------------

先说结论: 两者必须结合起来使用.

比如一个项目中的网络架构 VPC, 最好单独部署. 而 Application Stack, 里面涉及到支持 App 运行的 数据库, 消息队列, 等等, 最好用 Nested Stack 方式组织.

Nested Stack 不是万能的, 因为 CloudFormation 有参数个数, 资源个数的限制. 如果使用 Nested Stack, 这样位于 Master Template 的 Parameter 则是所有 Child Template 的 Parameter 的总和, 很容易超过 60 个.

参考资料:

- CloudFormation Limit: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html
- 60 Parameters per stack
- 60 Outputs per stack
