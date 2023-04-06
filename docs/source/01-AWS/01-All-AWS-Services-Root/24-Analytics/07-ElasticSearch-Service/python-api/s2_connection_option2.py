# -*- coding: utf-8 -*-

"""
use elasticsearch-dsl

**中文文档**

使用 ORM
"""

from datetime import datetime

import boto3
from elasticsearch import RequestsHttpConnection
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text, Index
from elasticsearch_dsl import connections
from requests_aws4auth import AWS4Auth
from superjson import json


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
connections.create_connection(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

html_strip = analyzer(
    "html_strip",
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


class Comment(InnerDoc):
    author = Text(fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    created_at = Date() # type: datetime

    def age(self):
        return datetime.now() - self.created_at


class Post(Document):
    title = Text()
    title_suggest = Text()
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer=html_strip,
        fields={"raw": Keyword()}
    )

    comments = Nested(Comment)

    class Index:
        name = "blog"

    def add_comment(self, author, content):
        self.comments.append(
            Comment(author=author, content=content, created_at=datetime.now()))

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super(Post, self).save(**kwargs)


def document_crud():
    # create the mappings in Elasticsearch
    Post.init()

    # instantiate the document
    # first = Post(title='My First Blog Post, yay!', published=True)
    # # assign some field values, can be values or lists of values
    # first.category = ['everything', 'nothing']
    # first.add_comment('me', 'This is nice!')
    #
    # # every document has an id in meta
    # first.meta.id = 47
    #
    # # save the document into the cluster
    # first.save()

    # retrieve the document
    # first = Post.get(id=47)
    # jprint(first.meta.to_dict())
    # jprint(first.to_dict())


document_crud()

def index_crud():
    blogs = Index("blog")

    # delete the index, ignore if it doesn't exist
    blogs.delete(ignore=404)

# index_crud()