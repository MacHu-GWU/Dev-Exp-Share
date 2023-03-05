#!/bin/bash

# This shell script allows you to quickly set your aws cli default profile to
# the temp credential retrieved from aws cli mfa authentication.
# Avoid manually edit ~/.aws/credential and ~/.aws/config file.
#
# Usage:
#
#   . ./awscli-mfa-auth.sh $source_aws_profile $mfa_token
#
# Then you can test with this command:
#
#   aws s3 ls
#
# By default it should use the temp MFA credential
#
# Requires:
#
# - aws cli
# - python
# - jq
#
# Reference:
# - How do I use an MFA token to authenticate access to my AWS resources through the AWS CLI?: https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/

if [ -n "${BASH_SOURCE}" ]
then
    dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
fi

aws_profile="$1"
mfa_token="$2"
aws_region=$(aws configure get region --profile $aws_profile)

caller_identity_response=$(aws sts get-caller-identity --profile $aws_profile)
aws_account_id=$(echo $caller_identity_response | jq '.Account' -r)
iam_user_arn=$(echo $caller_identity_response | jq '.Arn' -r)
mfa_device_arn=$(python -c "print('${iam_user_arn}'.replace(':user/', ':mfa/'))")

echo "retrive temp session token from $mfa_device_arn ..."
get_session_token_response=$(aws sts get-session-token --serial-number $mfa_device_arn --token-code $mfa_token --profile $aws_profile)

AWS_ACCESS_KEY_ID="$(echo $get_session_token_response | jq '.Credentials.AccessKeyId' -r)"
AWS_SECRET_ACCESS_KEY="$(echo $get_session_token_response | jq '.Credentials.SecretAccessKey' -r)"
AWS_SESSION_TOKEN="$(echo $get_session_token_response | jq '.Credentials.SessionToken' -r)"
AWS_DEFAULT_REGION="$aws_region"
AWS_DEFAULT_OUTPUT="json"

echo "inject temp credential into environment variable ..."
export AWS_PROFILE="${aws_profile}_mfa"
export AWS_DEFAULT_PROFILE="${aws_profile}_mfa"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AWS_SESSION_TOKEN="${AWS_SESSION_TOKEN}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}"
export AWS_DEFAULT_OUTPUT="${AWS_DEFAULT_OUTPUT}"

echo "inject temp credential into $HOME/.aws/credentials and $HOME/.aws/config file ..."
python "${dir_here}/awscli_mfa_update_credential.py" "${aws_profile}" "${AWS_ACCESS_KEY_ID}" "${AWS_SECRET_ACCESS_KEY}" "${AWS_SESSION_TOKEN}" "${aws_region}"
