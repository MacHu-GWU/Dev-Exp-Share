How to Manage Config in Single Place, Use it Everywhere for Any Tools
==============================================================================

Description of the Problem

Let’s think about this use case:

You have a microservice application called skymap, and it has multiple deployment stage dev, test, stage, qa, prod. Each stage will be placed into separate, independent environments and not talking to each other. So you probably want to use <app-name>-<stage> e.g. skymap-test as a prefix for all of your AWS Resource, such as VPC, S3 Bucket, Tag.

In your application code you might have something like:

# python code
app_name = "skymap"
stage = "test"
stack_name = f"{app_name}-{stage}" # CloudFormation Stack

In your shell script, you might have something like:

# shell scripts
app_name="skymap"
stage="test"
stack_name="${app_name}-${stage}"
aws cloudformation deploy --stack-name ${stack_name}

In your CloudFormation Template, you might need:

{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "AppName": {
            "Type": "string"
        },
        "Stage": {
            "Type": "string"
        }
    },
    "Resources": {
        "DeploymentBucket": {
            ...
            "BucketName": {
                "Fn::Sub": [
                    "${AppName}-${Stage}-deployment",
                    {
                        "AppName": {
                            "Ref": "AppName"
                        },
                        "Stage": {
                            "Ref": "Stage"
                        }
                    }
                ]
            }
        }
    }
}

In your serverless.yml, you might have this, and you have to pass options to serverless command:

...

provider:
  name: aws
  deploymentBucket:
    name: ${opt:app_name}-${opt:stage}-deployment

The stack_name and deployment_bucket_name are derived variables which depend on app_name and stage. But you have to maintain the transformation logic in FOUR DIFFERENCE PLACE! This is a highly denied Anti-Design-Pattern. Once you changed one place, it is very easy to forget to apply the change everywhere else.

Analysis of the Problem

The major reason behind this problem is because of:

some config value are generic config and not depend on any other config value. some other config value are derived value.

the entire configuration is used by multiple code component, such as application code, shell script, tools, or other config file.

those code components are not natively talk to each other, and not very easy to reference each other. For example, if you put the logic in Terraform, then you have to put some code in your application to parse terraform scripts and load the config into the memory.

And it finally ends up with maintaining same transform/reference logic at multiple places.

The Solution

Create a config-test.json file, put it anywhere you like, you could also create additional config files config-dev.json, config-stage.json, config-qa.json, config-prod.json:

# content of config-test.json file
{
    "APP_NAME": "skymap:,
    "STAGE": "test"
}

Create a config.py file put it under your repo root dir:

# content of config.py file

"""
If it is not Python Project, put this script at the repo root dir.
If it is a Python project, put into your python package dir, and allow other module to import this module.
For example::

    from .config import Config
    Config.initialize_config()
"""

import os
import json

# where the generic raw config file locate
RAW_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")

APP_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config-application.json")
SHELL_SCRIPT_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config-shell-script.json")
SERVERLESS_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config-serverless.json")
CLOUDFORMATION_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config-cloudformation.json")


class Config(object):
    # generic config
    APP_NAME = None
    STAGE = None
    
    # derived config
    ENVIRONMENT_NAME = None
    
    @classmethod
    def get_environment_name(cls)
        if cls.ENVIRONMENT_NAME is None:
            cls.ENVIRONMENT_NAME = "{app_name}-{stage}".format(
                app_name=cls.APP_NAME,
                stage=cls.STAGE,
            )
        return cls.ENVIRONMENT_NAME
        
    STACK_NAME = None
    
    @classmethod
    def get_stack_name(cls):
        if cls.STACK_NAME is None:
            cls.STACK_NAME = cls.get_environment_name()
        return cls.STACK_NAME
        
    DEPLOYMENT_BUCKET_NAME = None
    
    @classmethod
    def get_deployment_bucket_name(cls):
        if cls.DEPLOYMENT_BUCKET_NAME is None:
            cls.DEPLOYMENT_BUCKET_NAME = "{env_name}-deployment".format(
                env_name=cls.get_environment_name(),
            )
        return cls.DEPLOYMENT_BUCKET_NAME
        
    # basically you can copy and paste everything below this
    # you only need to focus on customizing your own logic   
    @classmethod
    def update_from_generic_config_file(cls):
        """inject config value in config.json file into this Config class
        """
        with open(RAW_CONFIG_FILE_PATH, "rb") as f:
            config_data = json.loads(f.read().decode("utf-8"))
        for attr, _ in cls.__dict__.items():
            if attr in config_data:
                setattr(cls, attr)
                
    @classmethod
    def derive_other_config_value(cls):
        """execute all config tranform funtions that starts with ``.get_xxx``
        """
        for attr, value in cls.__dict__.items():
            if attr.startswith("get_"):
                getattr(cls, attr)()
                
    @classmethod
    def to_config_data(cls):
        """extract all config value, generic and derived, put them into 
        a dictionary.
        """
        data = dict()
        for attr, value in cls.__dict__.items():
            if (not attr.startswith("_")) and (isinstance(value, str) or isinstance(value, int)):
                data[attr] = value
        return data
        
    to_appliation_config_data = to_config_data
    to_shell_scripts_config_data = to_config_data
    to_severless_config_data = to_config_data
        
    @classmethod
    def to_cloudformation_parameters_data(cls):
        data = cls.to_config_data()
        parameters = dict(
            AppName=cls.APP_NAME,
            Stage=cls.STAGE,
            EnvironmentName=cls.ENVIRONMENT_NAME,
            StackName=cls.STACK_NAME,
            DeploymentBucketName=cls.DEPLOYMENT_BUCKET_NAME,
        )
        return parameters
        
    @classmethod
    def initialize_config(cls):
        cls.update_from_generic_config_file()
        cls.derive_other_config_value()
        
        def dump_json(data, json_file):
            with open(json_file, "wb") as f:
                f.write(json.dumps(data, indent=4, sort_keys=True).encode("utf-8"))

        dump_json(cls.to_appliation_config_data(), APP_CONFIG_FILE_PATH)                
        dump_json(cls.to_shell_scripts_config_data(), SHELL_SCRIPT_CONFIG_FILE_PATH)
        dump_json(cls.to_severless_config_data(), SERVERLESS_CONFIG_FILE_PATH)
        dump_json(cls.to_cloudformation_parameters_data(), CLOUDFORMATION_CONFIG_FILE_PATH)
        
if __name__ == "__main__":
    Config.initialize_config()


After you called python config.py, you will see 4 additional files been created, config-application.json, config-shell-script.json, config-serverless.json, config-cloudformation.json.

Content of config-application.json, config-shell-script.json, config-serverless.json:

{
    "APP_NAME": "skymap",
    "STAGE": "test",
    "ENVIRONMENT_NAME": "skymap-test",
    "STACK_NAME": "skymap-test",
    "DEPLOYMENT_BUCKET_NAME": "skymap-test-deployment"
}

Content of config-cloudformation.json

{
    "AppName": "skymap",
    "Stage": "test",
    "EnvironmentName": "skymap-test",
    "StackName": "skymap-test",
    "DeploymentBucketName": "skymap-test-deployment"
}

Now your Shell Scripts becomes this:

# shell scripts
config_file="./config-shell-script.json"

# this function doesn't need anything
get_config_value_v1() {
    local config_key="$1"
    python -c "import json; data = json.loads(open('${config_file}', 'rb').read().decode('utf-8')); print(data['${config_key}'])"
}

# this function need jq command line 
get_config_value_v2() {
    local config_key=$1
    cat ${config_file} | jq .$config_key -r
}

app_name=$(get_config_value_v1 "APP_NAME")
stage=$(get_config_value_v1 "STAGE")
stack_name=$(get_config_value_v1 "STACK_NAME")

Your CloudFormation template becomes this:

{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "AppName": {
            "Type": "string"
        },
        "Stage": {
            "Type": "string"
        },
        "DeploymentBucketName": {
            "Type": "string"
        }
    },
    "Resources": {
        "DeploymentBucket": {
            ...
            "BucketName": {
                "Ref": "DeploymentBucketName"
            }
        }
    }
}

Your serverless.yml becomes this, and you don’t need to pass options to serverless deploy command anymore:

...

provider:
  name: aws
  deploymentBucket:
    name: ${file(./config-serverless.json):DEPLOYMENT_BUCKET_NAME}

And you can put arbitrary logic in your Shell Scripts / CICD Scripts like this:

# content of deploy.sh

# step1, copy specified generic config json file to repo root dir
cp <path-to-generic-config-file-dir/config.test.json> config.json

# step2, call config.py script, read config.json derive other config value
# generate additional config file for shell scripts, serverless, cloudformation
# etc ...
python config.py

# do what every you want to do,
...

Why This is a Good Design Pattern

Easy to maintain, with one-time setup, you only need to focus on your config value transform logic in config.py file and maintain your generic config-<stage>.json file.

Easy to customize and extend, unlike the way of Shell Scripts, CloudFormation, Severless, CloudFormation using their own dialect markup to handling variables, Python a full-featured programming language. Implement transform logic in python is way more human-readable and flexible.

There’s no assumption of where you store your generic config file, you can put it securely anywhere you want and just copy that to <repo_root_dir>/config.json to start.

FAQ

Why json? Why not .xml, .yml, .ini, .cfg?: Because it is super easy to read the value from JSON file on any OS (Windows has CONVERTFROM_JSON, Unix Based has built-in Python, or jq. Most of the other formats depend on external tools. And most of the high-level DevOps tools natively support JSON. Using JSON gives us the flexibility to integrate this pattern with any software, any project, any programming language.

Why put transform logic in Python?: Because unix based system has built-in Python. Python might be the easiest full-feature general programming language. It allows developer with No Python experience to be capable to implement their custom config value transform logic.

Why use the config.py?: Because it doesn’t require any dependencies. So it can be executed by PowerShell / Bash. Integrate the Config Initializer with other tools is very easy.