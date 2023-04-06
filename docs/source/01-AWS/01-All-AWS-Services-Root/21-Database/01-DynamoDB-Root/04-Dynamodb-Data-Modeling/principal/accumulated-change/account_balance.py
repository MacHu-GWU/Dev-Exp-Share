# -*- coding: utf-8 -*-

"""
有的时候需要保存每一个对象的所有历史修改记录. Dynamodb 可以用 sort_key 来实现这一点.
"""

import os
import random
from datetime import datetime

import pynamodb
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.models import Model

os.environ["AWS_PROFILE"] = "eq_sanhe"

connection = Connection()

epoch = "1970-01-01 00:00:00.000000"

TRANS_CREATE_ACCOUNT = "create-account"


class AccountBalanceModel(Model):
    """
    一个文档, 文档有不同的版本. 我们每次对文档进行更新, 实际上是建立一个新的版本.
    """
    class Meta:
        table_name = "accumulated-change-account-balance-1"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    account_id = UnicodeAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    trans_id = UnicodeAttribute(default=None)
    other_account_id = UnicodeAttribute()
    balance_change = NumberAttribute()
    description = UnicodeAttribute()

    @classmethod
    def create_account(cls, account_id, batch=None):
        """
        """
        try: # account is taken
            cls.query(hash_key=account_id).next()
            raise ValueError
        except StopIteration: # account_id not taken
            ab = cls(
                account_id=account_id,
                timestamp=str(datetime.now()),
                trans_id=TRANS_CREATE_ACCOUNT,
                description="create new account",
                amount_change=0
            )
            if batch is None:
                ab.save()
            else:
                batch.save(ab)

    @classmethod
    def create_transaction(cls,
                           account_id,
                           timestamp,
                           trans_id,
                           description,
                           amount_change,
                           batch=None):
        ab = cls(
            account_id=account_id,
            timestamp=timestamp,
            trans_id=trans_id,
            description=description,
            amount_change=amount_change,
        )
        if batch is None:
            ab.save()
        else:
            batch.save(ab)

AccountBalanceModel.create_table(wait=True)


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


def create_dummy_data():
    n_account = 10
    n_transaction_lower = 5
    n_transaction_upper = 10

    with AccountBalanceModel.batch_write() as batch:
        for account_id in range(1, 1+n_account):
            account_id = f"a-{account_id}"
            try:
                AccountBalanceModel.create_account(account_id=account_id)
            except:
                pass
            n_trans = random.randint(n_transaction_lower,n_transaction_upper)
            for transaction_id in range(1, 1+n_trans):
                trans_id = f"{account_id}-t-{transaction_id}"
                AccountBalanceModel.create_transaction(
                    account_id=account_id,
                    timestamp=str(datetime.utcnow()),
                    trans_id=trans_id,
                    description="",
                    amount_change=random.randint(-100, 100),
                    batch=batch,
                )

    # with DocumentModel.batch_write() as batch:
    #     for doc_id in range(1, 1 + n_document):
    #         for version_id in range(1, 1 + random.randint(1, max_version)):
    #             print(f"doc_id = {doc_id}, version_id = {version_id}")
    #             batch.save(
    #                 DocumentModel(
    #                     doc_id=f"d-{doc_id}",
    #                     version_id=version_id,
    #                     content=f"d-{doc_id} v-{version_id}",
    #                 )
    #             )

create_dummy_data()


def delete_all_tables():
    AccountBalanceModel.delete_table()


# delete_all_tables()

def get_doc_latest_version_id():
    print(BQuery.get_doc_latest_version_id(doc_id="d-1"))


# get_doc_latest_version_id()

def get_doc_nth_latest_content():
    print(BQuery.get_doc_nth_latest_content(doc_id="d-1", nth=2))

# get_doc_nth_latest_content()
