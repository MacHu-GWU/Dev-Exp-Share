# -*- coding: utf-8 -*-

import boto3
from rich import print
from opensearchpy import OpenSearch, RequestsHttpConnection
# from elasticsearch import Elasticsearch, RequestsHttpConnection
# from elasticsearch_dsl import connections
from requests_aws4auth import AWS4Auth

aws_profile = "aws_data_lab_sanhe"
aws_region = "us-east-1"
aws_service = "es"
endpoint = "search-sanhe-dev-ce5xh5zovkiwjkf2x4c4k2saf4.us-east-1.es.amazonaws.com"

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

print(es.info())
document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}
print(es.index(index="movies", id="5", body=document))
# from opensearchpy.client.
# print(es.get(index="movies", doc_type="_doc", id="5"))
res = es.search(
    index="movies",
    body={
        "query": {
            "match_all": {}
        }
    }
)
print(res)
# es = Elasticsearch(
#     hosts=[{"host": endpoint, "port": 443}],
#     http_auth=awsauth,
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# )

# username = "sanhe"
# password = "vEeGv9Xt7%p9"
# es_uri = f"https://{username}:{password}@{endpoint}:443/"
# es = Elasticsearch(
#     hosts=es_uri,
#     # http_auth=("sanhe", ),
#     use_ssl=True,
#     # url_prefix="",
#     # timeout=10,
#     # headers=None,
#     # http_compress=None,
#     # cloud_id=None,
#     # api_key=None,
#     # opaque_id=None,
#     # meta_header=True,
#     # **kwargs
# )
# print(es.info())
