# -*- coding: utf-8 -*-

"""
Generate the ssh command to connect to ec2 for you.

You have to put your ec2 key pair (.pem) file at ${HOME}/${AWS_ACCOUNT_ALIAS}/${AWS_REGION}/${KEY_NAME}

Ref:

- Default user name for AMI: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connection-prereqs.html#connection-prereqs-get-info-about-instance

- For Amazon Linux 2 or the Amazon Linux AMI, the user name is ec2-user.
- For a CentOS AMI, the user name is centos.
- For a Debian AMI, the user name is admin.
- For a Fedora AMI, the user name is ec2-user or fedora.
- For a RHEL AMI, the user name is ec2-user or root.
- For a SUSE AMI, the user name is ec2-user or root.
- For an Ubuntu AMI, the user name is ubuntu.
"""

import boto3
from pathlib import Path

# ------------------------- File in value here -------------------------
aws_profile = "your_aws_profile"
aws_region = "us-east-1"
ec2_name = ""
# ----------------------------------------------------------------------
print(f"try to create the ssh connect command for the ec2 {ec2_name!r} ...")

boto_ses = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)
ec2_client = boto_ses.client("ec2")
iam_client = boto_ses.client("iam")


def get_aws_account_alias() -> str:
    return iam_client.list_account_aliases()["AccountAliases"][0]


def get_instance_dict(ec2_name: str) -> dict:
    res = ec2_client.describe_instances(
        Filters=[
            dict(
                Name="tag:Name",
                Values=[
                    ec2_name,
                ]
            )
        ]
    )
    inst_dict = res["Reservations"][0]["Instances"][0]
    return inst_dict


def get_image_name(image_id: str) -> str:
    image_dct = ec2_client.describe_images(
        ImageIds=[image_id, ]
    )["Images"][0]
    image_name = image_dct["Name"]
    return image_name


aws_account_alias = get_aws_account_alias()
instance_dict = get_instance_dict(ec2_name)
public_ip = instance_dict["PublicIpAddress"]
image_id = instance_dict["ImageId"]
key_name = instance_dict["KeyName"]
image_name = get_image_name(image_id)

pem_file_path = (
    Path.home().absolute()
    / "ec2-pem"
    / aws_account_alias
    / aws_region
    / f"{key_name}.pem"
)

if image_name.startswith("amzn"):
    username = "ec2-user"
elif image_name.startswith("RHEL"):
    username = "ec2-user"
elif image_name.startswith("suse"):
    username = "ec2-user"
elif image_name.startswith("fedora"):
    username = "ec2-user"
elif image_name.startswith("ubuntu"):
    username = "ubuntu"
elif image_name.startswith("debian"):
    username = "admin"
else:
    username = "ec2-user"

cmd = "ssh -i {ec2_pem} {username}@{public_ip}".format(
    ec2_pem=pem_file_path, username=username, public_ip=public_ip,
)
if pem_file_path.exists():
    print("enter the following command to terminal:")
    print()
    print(cmd)
else:
    raise FileNotFoundError(f"{pem_file_path} not found!")
