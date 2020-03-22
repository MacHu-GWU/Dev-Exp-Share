#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Display running AWS Resource associate by Search Keyword.

- EC2: check all tag values
- Sagemake Notebook: check notebook name and all tag values
- RDS: check db identifier and all tag values
"""

import boto3


def tag_transform(tags_field):
    return {dct["Key"]: dct["Value"] for dct in tags_field}


def collect_running_ec2_instance(ec2_client, cf_client, detected_ec2, name_keyword, aws_account_id, region_name):
    # Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    res_ec2_describe_instances = ec2_client.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": [
                    "running",
                ]
            },
        ],
        MaxResults=1000,
    )

    try:
        assert isinstance(res_ec2_describe_instances["Reservations"][0]["Instances"], list)
    except:
        return

    for inst_data in res_ec2_describe_instances["Reservations"][0]["Instances"]:
        # test if it is created by User
        tags = tag_transform(inst_data["Tags"])

        instance_id = inst_data["InstanceId"]
        instance_name = tags.get("Name", "NA")

        url = "https://console.aws.amazon.com/ec2/home?region={}#Instances:instanceId={}".format(
            region_name, instance_id
        )

        tag_test_matched_flag = False
        for k, v in tags.items():
            if name_keyword.lower() in v.lower():
                # if True:
                tag_test_matched_flag = True
                tag_key = k
                tag_value = v
                break

        if tag_test_matched_flag:
            msg = "  - Account = {}, Region = {}, Id = '{}', Name = '{}'. Detected  by Tag '{}' = '{}'. Open in Console = {}".format(
                aws_account_id, region_name, instance_id, instance_name, tag_key, tag_value, url
            )
            detected_ec2.append(msg)
            continue

        # test if it is created by cloudformation stack
        if "aws:cloudformation:stack-name" in tags:
            stack_name = tags["aws:cloudformation:stack-name"]
            res_cf_describe_stacks = cf_client.describe_stacks(StackName=stack_name)
            stack_tags = tag_transform(res_cf_describe_stacks["Stacks"][0]["Tags"])
            tag_test_matched_flag = False
            for k, v in stack_tags.items():
                if name_keyword.lower() in v.lower():
                    # if True:
                    tag_test_matched_flag = True
                    tag_key = k
                    tag_value = v
                    break

            if tag_test_matched_flag is True:
                msg = "  - Account = {}, Region = {}, Id = '{}', Name = '{}'. Detected by Stack = '{}', Stack Tag '{}' = '{}'. Open in Console = {}".format(
                    aws_account_id, region_name, instance_id, instance_name, stack_name, tag_key, tag_value, url
                )
                detected_ec2.append(msg)


def collect_running_notebook_instance(smkr_client, detected_notebook, name_keyword, aws_account_id, region_name):
    res_smkr_list_notebook_instances = smkr_client.list_notebook_instances(
        StatusEquals="InService",
        MaxResults=100,
    )
    try:
        assert isinstance(res_smkr_list_notebook_instances["NotebookInstances"], list)
    except:
        return

    for notebook_data in res_smkr_list_notebook_instances["NotebookInstances"]:
        # use name
        notebook_name = notebook_data["NotebookInstanceName"]
        notebook_arn = notebook_data["NotebookInstanceArn"]
        url = "https://console.aws.amazon.com/sagemaker/home?region={}#/notebook-instances/{}".format(
            region_name, notebook_name
        )

        # use tags
        res_smkr_list_tags = smkr_client.list_tags(ResourceArn=notebook_arn)
        notebook_tags = tag_transform(res_smkr_list_tags["Tags"])

        if name_keyword.lower() in notebook_name.lower():
            msg = "  - Account = {}, Region = {}, Notebook = '{}'. Detected by Name = '{}'. Open in Console = {}".format(
                aws_account_id, region_name, notebook_name, notebook_name, url
            )
            detected_notebook.append(msg)
            continue

        tag_test_matched_flag = False
        for k, v in notebook_tags.items():
            if name_keyword.lower() in v.lower():
                tag_test_matched_flag = True
                tag_key = k
                tag_value = v
                break

        if tag_test_matched_flag is True:
            msg = "  - Account = {}, Region = {}, Notebook = '{}'. Detected by Tags '{}' = '{}'. Open in Console = {}".format(
                aws_account_id, region_name, notebook_name, tag_key, tag_value, url
            )
            detected_notebook.append(msg)


def collect_running_rds(rds_client, detected_rds, name_keyword, aws_account_id, region_name):
    # Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.describe_db_instances
    res_rds_describe_db_instances = rds_client.describe_db_instances(
        Filters=[
        ],
        MaxRecords=100,
    )

    try:
        assert isinstance(res_rds_describe_db_instances["DBInstances"], list)
    except:
        return

    for db_inst_data in res_rds_describe_db_instances["DBInstances"]:
        # use name
        db_name = db_inst_data["DBInstanceIdentifier"]
        db_inst_arn = db_inst_data["DBInstanceArn"]

        url = "https://console.aws.amazon.com/rds/home?region={}#database:id={}".format(
            region_name, db_name
        )

        if name_keyword.lower() in db_name.lower():
            msg = "  - Account = {}, Region = {}, RDS Inst = '{}'. Detected by Name = '{}'. Open in Console = {}".format(
                aws_account_id, region_name, db_name, db_name, url
            )
            detected_rds.append(msg)
            continue

        # use tags
        # Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.list_tags_for_resource
        res_smkr_list_tags_for_resource = rds_client.list_tags_for_resource(ResourceName=db_inst_arn)
        db_inst_tags = tag_transform(res_smkr_list_tags_for_resource["TagList"])

        tag_test_matched_flag = False
        for k, v in db_inst_tags.items():
            if name_keyword.lower() in v.lower():
                tag_test_matched_flag = True
                tag_key = k
                tag_value = v
                break

        if tag_test_matched_flag is True:
            msg = "  - Account = {}, Region = {}, RDS Inst = '{}'. Detected by Tags '{}' = '{}'. Open in Console = {}".format(
                aws_account_id, region_name, db_name, tag_key, tag_value, url
            )
            detected_rds.append(msg)


def main(name_keyword, aws_profile, region_list):
    client = boto3.session.Session(profile_name=aws_profile).client("sts")
    aws_account_id = client.get_caller_identity()["Account"]

    detected_ec2 = list()
    detected_notebook = list()
    detected_rds = list()

    for region_name in region_list:
        boto_session = boto3.session.Session(profile_name=aws_profile, region_name=region_name)

        ec2_client = boto_session.client("ec2")
        cf_client = boto_session.client("cloudformation")
        smkr_client = boto_session.client("sagemaker")
        rds_client = boto_session.client("rds")

        # --- detect ec2 ---
        collect_running_ec2_instance(
            ec2_client, cf_client, detected_ec2,
            name_keyword, aws_account_id, region_name,
        )

        # --- detect notebook instance ---
        collect_running_notebook_instance(
            smkr_client, detected_notebook,
            name_keyword, aws_account_id, region_name,
        )

        # --- detect notebook instance ---
        collect_running_rds(
            rds_client, detected_rds,
            name_keyword, aws_account_id, region_name,
        )

    if len(detected_ec2):
        print("running ec2 instance:")
        for msg in detected_ec2:
            print(msg)

    if len(detected_notebook):
        print("running notebook instance:")
        for msg in detected_notebook:
            print(msg)

    if len(detected_rds):
        print("running rds instance:")
        for msg in detected_rds:
            print(msg)


if __name__ == "__main__":
    # Search Keyword
    name_keyword = "sanhe"

    # AWS Profile you are using
    aws_profile = "eqtest"

    # AWS Region List
    region_list = [
        "us-east-1",
        "us-east-2",
    ]
    main(name_keyword, aws_profile, region_list)
