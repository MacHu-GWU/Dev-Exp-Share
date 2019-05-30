#!/bin/bash

stack_name="my-service-dev"
aws_profile="skymap_sandbox"

packge() {
    aws cloudformation package \
        --template-file my-service.json \
        --s3-bucket skymap-sandbox-cloudformation-script \
        --use-json \
        --s3-prefix "${stack_name}" \
        --output-template-file packaged.json \
        --force-upload \
        --profile $aws_profile
}

deploy() {
    parameter_overrides="$(python convert_parameters.py config.json)"
    aws cloudformation deploy \
        --template-file packaged.json \
        --stack-name $stack_name \
        --tags creator="Sanhe" \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides $parameter_overrides \
        --profile $aws_profile
}

packge
deploy
