# -*- coding: utf-8 -*-

from pathlib import Path

import boto3
import lakeformation as lf

import resource_669508176277_us_west_1 as r
import principal_669508176277 as p

profile_name = "aws_data_lab_sanhe"
region_name = "us-west-1"
boto_ses = boto3.session.Session(profile_name=profile_name, region_name=region_name)
dir_here = Path(__file__).absolute().parent
pb = lf.Playbook(boto_ses=boto_ses, workspace_dir=str(dir_here))

# ------------------------------------------------------------------------------
# Tag
# ------------------------------------------------------------------------------
prefix = "aws_lf_tag"

tag_admin_access_y = lf.LfTag(key=f"{prefix}_admin_access", value="y", pb=pb)
tag_admin_access_n = lf.LfTag(key=f"{prefix}_admin_access", value="n", pb=pb)
tag_regular_access_y = lf.LfTag(key=f"{prefix}_regular_access", value="y", pb=pb)
tag_regular_access_n = lf.LfTag(key=f"{prefix}_regular_access", value="n", pb=pb)
tag_limited_access_y = lf.LfTag(key=f"{prefix}_limited_access", value="y", pb=pb)
tag_limited_access_n = lf.LfTag(key=f"{prefix}_limited_access", value="n", pb=pb)


# ------------------------------------------------------------------------------
# Resource
#
# all database name / table name / column name are automatically generated
# you can leverage text editor auto complete feature in
# VScode / Sublime / PyCharm / Notepad ++ or any
# to access a resource variable
# ------------------------------------------------------------------------------
pb.attach(r.db_669508176277_us_west_1_lf_sme_demo_db, tag_admin_access_y)

pb.attach(r.db_669508176277_us_west_1_lf_sme_demo_db, tag_regular_access_y)
pb.attach(r.col_669508176277_us_west_1_lf_sme_demo_db_users_ssn, tag_regular_access_n)

pb.attach(r.db_669508176277_us_west_1_lf_sme_demo_db, tag_limited_access_y)
pb.attach(r.tb_669508176277_us_west_1_lf_sme_demo_db_items, tag_limited_access_n)


# ------------------------------------------------------------------------------
# Principal
#
# all IAM user / role principal are automatically generated
# same as resource, you can leverage text editor auto complete feature
# ------------------------------------------------------------------------------
pb.grant(p.role_lf_sme_demo_admin, tag_admin_access_y,
         [lf.SuperDatabase, lf.SuperDatabaseGrantable, lf.SuperTable, lf.SuperTableGrantable])
pb.grant(p.role_lf_sme_demo_regular, tag_regular_access_y, [lf.DescribeDatabase, lf.DescribeTable, lf.Select])
pb.grant(p.role_lf_sme_demo_limited, tag_limited_access_y, [lf.DescribeDatabase, lf.DescribeTable, lf.Select])


# ------------------------------------------------------------------------------
# Apply all change
# ------------------------------------------------------------------------------
data = pb.serialize()
pb.apply(verbose=True, dry_run=False)
