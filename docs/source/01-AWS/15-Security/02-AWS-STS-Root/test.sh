#!/bin/bash

aws sts assume-role --role-arn arn:aws:iam::501105007192:role/codebuild-power-user --role-session-name codebuild_job_role
#data="$(aws sts get-session-token --duration-seconds 900)"
#AWS_ACCESS_KEY_ID="$(jq -r '.Credentials.SecretAccessKey' <<< "${data}")"
#AWS_SESSION_TOKEN="$(jq -r '.Credentials.SessionToken' <<< "${data}")"
