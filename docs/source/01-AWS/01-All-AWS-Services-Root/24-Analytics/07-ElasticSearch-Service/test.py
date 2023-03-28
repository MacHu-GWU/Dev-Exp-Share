# -*- coding: utf-8 -*-

import json

import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def jprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))

aws_profile = "eq_sanhe"
# boto_ses = boto3.Session(profile_name=aws_profile)
# es_client = boto_ses.client("es")

# res = es_client.list_domain_names()
# jprint(res)

host = 'search-eq-sanhe-elk-test-xtk75koc2og7hxvzsg4zmf55h4.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session(profile_name=aws_profile).get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

es.index(index="movies", doc_type="_doc", id="5", body=document)
print(es.get(index="movies", doc_type="_doc", id="5"))

# # Define a default Elasticsearch client
# HOME = os.path.expanduser("~")
# context = create_default_context(cafile=os.path.join(HOME, "ec2-pem/eq-sanhe-dev.pem"))
#
# connections.create_connection(
#     hosts=['search-eq-sanhe-elk-test-xtk75koc2og7hxvzsg4zmf55h4.us-east-1.es.amazonaws.com'],port=443,
#     ssl_context=context,
#     timeout=3
# )
#
# class Article(Document):
#     title = Text(analyzer='snowball', fields={'raw': Keyword()})
#     body = Text(analyzer='snowball')
#     tags = Keyword()
#     published_from = Date() # type: datetime
#     lines = Integer()
#
#     class Index:
#         name = 'blog'
#         settings = {
#           "number_of_shards": 2,
#         }
#
#     def save(self, ** kwargs):
#         self.lines = len(self.body.split())
#         return super(Article, self).save(** kwargs)
#
#     def is_published(self):
#         return datetime.now() >= self.published_from
#
# # create the mappings in elasticsearch
# Article.init()
#
# # create and save and article
# article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
# article.body = ''' looong text '''
# article.published_from = datetime.now()
# article.save()
#
# article = Article.get(id=42)
# print(article.is_published())
#
# # Display cluster health
# print(connections.get_connection().cluster.health())
#
#
