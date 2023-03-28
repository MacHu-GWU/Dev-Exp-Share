# -*- coding: utf-8 -*-

import boto3
from pathlib_mate import Path
from lakeformation import gen_resource, gen_principal

profile_name = "aws_data_lab_sanhe"
region_name = "us-west-1"
dir_here = Path(__file__).parent
boto_ses = boto3.session.Session(profile_name=profile_name, region_name=region_name)

gen_resource(boto_ses=boto_ses, workspace_dir=dir_here.abspath)
gen_principal(boto_ses=boto_ses, workspace_dir=dir_here.abspath)
