# -*- coding: utf-8 -*-

import boto3
import opensearchpy.exceptions
from rich import print
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

aws_profile = "aws_data_lab_sanhe"
aws_region = "us-east-1"
aws_service = "es"
endpoint = "search-sanhe-dev-ce5xh5zovkiwjkf2x4c4k2saf4.us-east-1.es.amazonaws.com"


def create_connection():
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


def single_document_crud(es):
    # --- Create / Replace
    post = {
        "title": "Hello ElasticSearch",
        "author": "Bennett Miller",
        "create_at": "2000-03-01",
        "update_at": "2000-03-05",
        "content": "Hello Alice",
        "like": 0
    }
    # this API can overwrite the entire document
    res = es.index(index="posts", id="1", body=post)
    assert res["result"] in ["created", "updated"]
    # print(res)
    # --- Get
    # get one document by id
    res = es.get(index="posts", id="1")
    assert res["found"] is True
    assert res["_source"] == post

    # if id not hit any results, it raise exception
    try:
        es.get(index="posts", id="2")
    except opensearchpy.exceptions.NotFoundError:
        pass

    # --- Update
    # update part of a document
    body = {
        "doc": {
            "content": "Hello Bob"
        },
    }
    res = es.update(index="posts", id="1", body=body)
    assert res["result"] == "updated"

    res = es.get(index="posts", id="1")
    assert res["_source"]["content"] == "Hello Bob"

    # use script to update document, you cannot use both ``script`` and ``body``
    # but you can put whatever you suppose to put in ``body`` within ``script``
    body = {
        "script": {
            "source": "ctx._source.like += 1; ctx._source.content = 'Hello Cathy'"
        }
    }
    res = es.update(index="posts", id="1", body=body)
    assert res["result"] == "updated"

    res = es.get(index="posts", id="1")
    assert res["_source"]["content"] == "Hello Cathy"
    assert res["_source"]["like"] == 1

    # --- Delete
    res = es.delete(index="posts", id="1")
    assert res["result"] == "deleted"

    try:
        es.get(index="posts", id="2")
    except opensearchpy.exceptions.NotFoundError:
        pass


def query_language(es):
    documents = [
        dict(
            text="php is the best programming language",
            create_date="2021-11-08",
            tag=["tech", "programming"],
        ),
        dict(
            text="Trump closed his twitter",
            create_date="2021-11-09",
            tag=["politics", "trump"]
        )
    ]
    for id, doc in enumerate(documents):
        es.index(index="news", id=str(id+1), body=doc)

    # body = {
    #     "query": {
    #         "term": {
    #             "text": "php"
    #         }
    #     }
    # }
    body = {
        "query": {
            "match": {
                "text": "trump"
            }
        }
    }
    # res = es.search(index="news", body=body)
    # print(res)
    # res = es.get(index="news")
    # print(res)

    print(es.indices.get_mapping(index="news"))

if __name__ == "__main__":
    es = create_connection()
    # single_document_crud(es)
    # query_language(es)

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
