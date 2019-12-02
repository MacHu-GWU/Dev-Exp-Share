# -*- coding: utf-8 -*-

"""
use elasticsearch-py

**中文文档**

使用 low level client,
"""

import boto3
from superjson import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def jprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))


aws_profile = "eq_sanhe"
host = "search-eq-sanhe-elk-test-xtk75koc2og7hxvzsg4zmf55h4.us-east-1.es.amazonaws.com"
region = "us-east-1"
service = "es"

# connect
credentials = boto3.Session(profile_name=aws_profile).get_credentials()
awsauth = AWS4Auth(
    credentials.access_key, credentials.secret_key, region, service,
    session_token=credentials.token,
)
es = Elasticsearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# create
document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}
es.index(index="movies", id="5", body=document)

# read
jprint(es.get(index="movies", doc_type="_doc", id="5"))
