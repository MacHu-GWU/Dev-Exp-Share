# -*- coding: utf-8 -*-

import boto3

aws_profile = "sanhe"
ses = boto3.Session(profile_name=aws_profile)
client = ses.client("dynamodb")

tname = "learn-dynamodb-users"


def put_test_data():
    client.put_item(
        TableName=tname,
        Item={
            "user_id": {
                "N": "1"
            },
            "username": {
                "S": "Alice"
            },
            "": {
                "N": "3"
            },
        }
    )
    client.put_item(
        TableName=tname,
        Item={
            "user_id": {
                "N": "2"
            },
            "username": {
                "S": "Bob"
            },
            "rank": {
                "N": "2"
            },
        }
    )
    client.put_item(
        TableName=tname,
        Item={
            "user_id": {
                "N": "3"
            },
            "username": {
                "S": "Cathy"
            },
            "rank": {
                "N": "1"
            },
        }
    )

def example_get_item():
    res = client.get_item(
        TableName=tname,
        Key={
            "user_id": {"N": "1"},
            "username": {"S": "Alice"},
        },
    )
    print(res)


def example_query():
    res = client.query(
        TableName=tname,
        IndexName="rank-index",
        KeyConditionExpression="rank = :rank",
        ExpressionAttributeValues={
            ":rank": {"N": "3"},
        }
    )
    print(res)

# put_test_data()
# example_get_item()
example_query()