# -*- coding: utf-8 -*-

"""
**中文文档**

- ES 数据类型文档: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
"""

import connect
from elasticsearch_dsl import (
    Index, Document, Text, Completion,
    analyzer
)
from superjson import json


def jprint(data):
    print(json.dumps(data, indent=4, sort_keys=True))


html_strip = analyzer("html_strip",
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


class BlogPost(Document):
    title = Text(analyzer=html_strip)
    title_suggest = Completion(analyzer=html_strip)

    class Index:
        name = "post"


def document_crud():
    # create the mappings in Elasticsearch
    BlogPost.init()

    # instantiate the document
    posts = [
        BlogPost(
            title="How to do full text search in ElasticSearch?",
            meta={"id": 1},
        ),
    ]
    for post in posts:
        post.title_suggest = post.title
        post.save()

    # retrieve the document
    def full_text_search_by_words():
        res = BlogPost.search() \
            .query("match", title="full") \
            .query("match", title="text") \
            .execute()
        jprint(res.to_dict())
        # assert len(list(res)) == 1
        # assert list(res)[0].meta.id == str(3)

    def full_text_search_by_auto_suggestion():
        # jprint(BlogPost.get(1).to_dict())
        res = BlogPost.search() \
            .suggest("suggested_title", "full", term={"field": "title_suggest"}) \
            .execute
        jprint(res.to_dict())
        for result in res.suggest.suggested_title:
            print('Suggestions for %s:' % result.text)
        #     for option in result.options:
        #         print('  %s (%r)' % (option.text, option.payload))
        # jprint(res.to_dict()) # # .query("match", tit le_suggest="full") \

    full_text_search_by_auto_suggestion()


document_crud()


def index_crud():
    blogs = Index("post")
    # delete the index, ignore if it doesn't exist
    blogs.delete(ignore=404)

# index_crud()
