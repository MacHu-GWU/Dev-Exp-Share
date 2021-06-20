# -*- coding: utf-8 -*-

"""
有的时候需要保存每一个对象的所有历史修改记录. Dynamodb 可以用 sort_key 来实现这一点.
"""

import os
import random

import pynamodb
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.models import Model

os.environ["AWS_PROFILE"] = "eq_sanhe"

connection = Connection()


class DocumentModel(Model):
    """
    一个文档, 文档有不同的版本. 我们每次对文档进行更新, 实际上是建立一个新的版本.
    """
    class Meta:
        table_name = "version-control-document-1"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    doc_id = UnicodeAttribute(hash_key=True)
    version_id = NumberAttribute(range_key=True)
    content = UnicodeAttribute()

    @classmethod
    def create_new_version(cls, doc_id, content):
        """
        """
        try:
            last_doc: DocumentModel = DocumentModel.query(hash_key=doc_id, scan_index_forward=False, limit=1).next()
            if content == last_doc.content: # duplicate content, no need to update
                raise ValueError
            new_version_id = last_doc.version_id + 1
        except StopIteration:
            new_version_id = 1

        cls(doc_id=doc_id, version_id=new_version_id, content=content).save()


DocumentModel.create_table(wait=True)


class BQuery:
    @classmethod
    def get_doc_latest_version_id(cls, doc_id):
        """
        获得文档最新版本的内容.
        """
        return DocumentModel.query(hash_key=doc_id, scan_index_forward=False, limit=1).next().version_id

    @classmethod
    def get_doc_nth_latest_content(cls, doc_id, nth):
        """
        获得文档最新版本第 N 新的内容.
        """
        if nth == 1:
            return DocumentModel.query(hash_key=doc_id, scan_index_forward=False, limit=1).next().content
        else:
            latest_version_id = cls.get_doc_latest_version_id(doc_id=doc_id)
            version_id = latest_version_id + 1 - nth
            return DocumentModel.get(hash_key=doc_id, range_key=version_id).content


def create_document_dummy_data():
    n_document = 1000
    max_version = 5
    with DocumentModel.batch_write() as batch:
        for doc_id in range(1, 1 + n_document):
            for version_id in range(1, 1 + random.randint(1, max_version)):
                print(f"doc_id = {doc_id}, version_id = {version_id}")
                batch.save(
                    DocumentModel(
                        doc_id=f"d-{doc_id}",
                        version_id=version_id,
                        content=f"d-{doc_id} v-{version_id}",
                    )
                )

# create_document_dummy_data()


def delete_all_tables():
    DocumentModel.delete_table()


# delete_all_tables()

def get_doc_latest_version_id():
    print(BQuery.get_doc_latest_version_id(doc_id="d-1"))


# get_doc_latest_version_id()

def get_doc_nth_latest_content():
    print(BQuery.get_doc_nth_latest_content(doc_id="d-1", nth=2))

# get_doc_nth_latest_content()
