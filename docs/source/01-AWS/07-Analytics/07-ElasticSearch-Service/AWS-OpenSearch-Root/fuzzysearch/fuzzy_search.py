# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import boto3
import typing
import opensearchpy.exceptions
from rich import print
from pathlib_mate import Path
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

aws_profile = "aws_data_lab_sanhe"
aws_region = "us-east-1"
aws_service = "es"
endpoint = "search-sanhe-dev-ce5xh5zovkiwjkf2x4c4k2saf4.us-east-1.es.amazonaws.com"


def create_connection(
    aws_profile,
    aws_region,
    aws_service,
    endpoint,
):
    credentials = boto3.Session(profile_name=aws_profile).get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key, credentials.secret_key, aws_region, aws_service,
        session_token=credentials.token,
    )
    es = OpenSearch(
        hosts=[{"host": endpoint, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    print(es.info())  # validate connection
    return es


def read_city_data(us_state_city_csv_file) -> typing.List[dict]:
    city_data = list()
    with open(us_state_city_csv_file, "r") as f:
        for line in f.readlines():
            state, city = line.strip().split("\t")
            city_dict = dict(
                state=state,
                city=city,
            )
            city_data.append(city_dict)
    return city_data


def insert_data(es, city_data):
    for city_dict in city_data:
        id_ = "{}-{}".format(city_dict["state"], city_dict["city"])
        print(f"working on {id_}")
        res = es.index(index="us_state_and_city", id=id_, body=city_dict)


us_state_city_csv_file = Path(__file__).change(new_basename="us_state_city.csv")
city_data = read_city_data(us_state_city_csv_file.abspath)

es = create_connection(aws_profile, aws_region, aws_service, endpoint)

insert_data(es, city_data)
