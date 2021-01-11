#!/bin/bash

# download kubectl
curl -o /tmp/kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/darwin/amd64/kubectl

# apply execute permissions to the binary.
sudo mv /tmp/kubectl /usr/local/bin
sudo chmod +x /usr/local/bin/kubectl

# download eksctl
curl --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

# move to /usr/local/bin
sudo mv /tmp/eksctl /usr/local/bin

#
eksctl version


CLUSTER_NAME="beautiful-creature-1607628346"
STACK_NAME=$(eksctl get nodegroup --cluster ${CLUSTER_NAME} -o json | jq -r '.[].StackName')

INSTANCE_PROFILE_ARN=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq -r '.Stacks[].Outputs[] | select(.OutputKey=="InstanceProfileARN") | .OutputValue')

ROLE_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME | jq -r '.Stacks[].Outputs[] | select(.OutputKey=="InstanceRoleARN") | .OutputValue' | cut -f2 -d/)

aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name FluentBit-DS \
    --policy-document file:///Users/sanhehu/Documents/GitHub/odp-container-audit-log-best-practice/eks-fluent-bit-daemonset-policy.json