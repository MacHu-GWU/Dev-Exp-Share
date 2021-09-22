#!/bin/bash


#aws glue get-resource-policy --resource-arn --profile aws_data_lab_sanhe

#aws_account_id="$(aws sts get-caller-identity | jq '.Account' -r)"
#echo $aws_account_id


#aws glue get-table --database lakeformation_access_poc --name users
aws glue tag-resource --resource-arn arn:aws:glue:region:669508176277:table/lakeformation_access_poc --tags-to-add MyName="Alice" --profile aws_data_lab_sanhe

