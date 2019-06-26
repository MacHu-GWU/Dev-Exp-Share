import json
import inspect


def convert_to_dct(klass):
    data = dict()
    for key, value in klass.__dict__.items():
        if not key.startswith("__"):
            if inspect.isclass(value):
                data[key] = convert_to_dct(value)
            else:
                data[key] = value
    return data


def convert_to_json(klass):
    return json.dumps(convert_to_dct(klass), sort_keys=True, indent=4)

#---
class Config:
    app_name = "webappt"
    stage = "dev"

    class DB:
        host = "localhost"  # hey description!
        port = 80

    environment_name = f"{app_name}-{stage}"


print(convert_to_json(Config))


class CloudFormationTRemplate:
    AWSTemplateFormatVersion = "2010-09-09"
    class Parameters:
        class EnvironmentName1:
            Type = "String"
            Description = "An"

        Description_Template = "An environment name that will be prefixed to resource names""
        class EnvironmentName2(EnvironmentName1):
            name1 = ""



"""
{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Metadata": {
        "Description": "This IAM Stack creates related Customer Managed Policy and IAM Role for use (Primarily Lambda)."
    },
    "Parameters": {
        "EnvironmentName": {
            "Type": "String",
            "Description": "An environment name that will be prefixed to resource names"
        },
        "ServiceName": {
            "Type": "String",
            "Description": "The name of this micro service"
        },
        "Stage": {
            "Type": "String",
            "Description": "the stage of this environment, one of dev, test, stage, qa, prod"
        },
        "LambdaDeployBucketName": {
            "Type": "String",
            "Description": "The S3 Bucket for lambda function deployment"
        }
    },
    "Resources": {
        "LambdaDeployBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "AccessControl": "Private",
                "BucketName": {
                    "Ref": "LambdaDeployBucketName"
                },
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": true,
                    "BlockPublicPolicy": true,
                    "IgnorePublicAcls": true,
                    "RestrictPublicBuckets": true
                },
                "Tags": [
                    {
                        "Key": "env",
                        "Value": {
                            "Ref": "EnvironmentName"
                        }
                    },
                    {
                        "Key": "stage",
                        "Value": {
                            "Ref": "Stage"
                        }
                    },
                    {
                        "Key": "project",
                        "Value": {
                            "Ref": "ServiceName"
                        }
                    }
                ]
            }
        }
    }
}
"""