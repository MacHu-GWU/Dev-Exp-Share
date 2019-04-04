# -*- coding: utf-8 -*-

import boto3
from pprint import pprint

aws_profile = "sanhe"
ses = boto3.Session(profile_name=aws_profile)
client = ses.client("dynamodb")

tname = "learn-dynamodb-gamescores"

test_data = [
    {
        "user_id": {"N": "101"},
        "game_title": {"S": "Galaxy Invaders"},
        "top_score": {"N": "5842"},
        "top_score_time": {"S": "2015-09-15 17:24:31"},
        "wins": {"N": "21"},
        "losses": {"N": "72"},
    },
    {
        "user_id": {"N": "101"},
        "game_title": {"S": "Meteor Blasters"},
        "top_score": {"N": "1000"},
        "top_score_time": {"S": "2015-10-22 23:18:01"},
        "wins": {"N": "12"},
        "losses": {"N": "3"},
    },
    {
        "user_id": {"N": "101"},
        "game_title": {"S": "Starship X"},
        "top_score": {"N": "24"},
        "top_score_time": {"S": "2015-08-31 13:14:21"},
        "wins": {"N": "4"},
        "losses": {"N": "9"},
    },
    {
        "user_id": {"N": "102"},
        "game_title": {"S": "Alien Adventure"},
        "top_score": {"N": "192"},
        "top_score_time": {"S": "2015-07-12 11:07:56"},
        "wins": {"N": "32"},
        "losses": {"N": "192"},
    },
    {
        "user_id": {"N": "102"},
        "game_title": {"S": "Galaxy Invaders"},
        "top_score": {"N": "0"},
        "top_score_time": {"S": "2015-09-18 07:33:42"},
        "wins": {"N": "0"},
        "losses": {"N": "5"},
    },
    {
        "user_id": {"N": "103"},
        "game_title": {"S": "Attack Ships"},
        "top_score": {"N": "3"},
        "top_score_time": {"S": "2015-09-18 07:33:42"},
        "wins": {"N": "1"},
        "losses": {"N": "8"},
    },
    {
        "user_id": {"N": "103"},
        "game_title": {"S": "Galaxy Invaders"},
        "top_score": {"N": "2317"},
        "top_score_time": {"S": "2015-09-18 07:33:42"},
        "wins": {"N": "40"},
        "losses": {"N": "3"},
    },
    {
        "user_id": {"N": "103"},
        "game_title": {"S": "Meteor Blasters"},
        "top_score": {"N": "723"},
        "top_score_time": {"S": "2015-09-18 07:33:42"},
        "wins": {"N": "22"},
        "losses": {"N": "12"},
    },
    {
        "user_id": {"N": "103"},
        "game_title": {"S": "Starship X"},
        "top_score": {"N": "42"},
        "top_score_time": {"S": "2015-09-18 07:33:42"},
        "wins": {"N": "12"},
        "losses": {"N": "19"},
    },
]


def insert_test_data():
    for item in test_data:
        client.put_item(
            TableName=tname,
            Item=item
        )


def example_query_what_is_top_score_ever_recorded_for_Meteor_Blasters():
    """
    highest = 1000
    lowest = 723
    :return:
    """
    res = client.query(
        TableName=tname,
        IndexName="game_title-top_score-index",
        KeyConditionExpression="game_title = :game_title",
        ExpressionAttributeValues={
            ":game_title": {"S": "Meteor Blasters"},
        },
        ScanIndexForward=False,
        Limit=1,
        ProjectionExpression="top_score"
    )
    pprint(res["Items"][0])
    assert len(res["Items"]) == 1


def example_query_which_user_had_the_highest_score_for_Galaxy_Invaders():
    """
    highest score user = 101
    lowest score user = 102
    :return:
    """
    res = client.query(
        TableName=tname,
        IndexName="game_title-top_score-index",
        KeyConditionExpression="game_title = :game_title",
        ExpressionAttributeValues={
            ":game_title": {"S": "Galaxy Invaders"},
        },
        ScanIndexForward=False,
        Limit=1,
        ProjectionExpression="user_id, top_score"
    )
    pprint(res["Items"][0])
    assert len(res["Items"]) == 1


def example_query_what_was_the_highest_ratio_of_wins_vs_losses():
    """
    highest score user = 101
    lowest score user = 102
    :return:
    """
    res = client.query(
        TableName=tname,
        IndexName="game_title-top_score-index",
        KeyConditionExpression="game_title = :game_title",
        ExpressionAttributeValues={
            ":game_title": {"S": "Galaxy Invaders"},
        },
        ScanIndexForward=False,
        Limit=1,
    )
    pprint(res["Items"][0])
    assert len(res["Items"]) == 1


def example_query():
    """
    Galaxy Invaders

    user_id wins    losses
    101     21      72
    102     0       5
    103     40      3
    """
    res = client.query(
        TableName=tname,
        IndexName="game_title-top_score-index",
        KeyConditionExpression="game_title = :game_title",
        ExpressionAttributeValues={
            ":game_title": {"S": "Galaxy Invaders"},
            ":wins": {"N": "0"},
        },
        FilterExpression="wins > :wins",
        # ScanIndexForward=False,
        # Limit=1,
    )
    pprint(res["Items"])

# example_query_what_is_top_score_ever_recorded_for_Meteor_Blasters()
# example_query_which_user_had_the_highest_score_for_Galaxy_Invaders()
# example_query_what_was_the_highest_ratio_of_wins_vs_losses()
example_query()

"""
What was the highest ratio of wins vs. losses?
"""