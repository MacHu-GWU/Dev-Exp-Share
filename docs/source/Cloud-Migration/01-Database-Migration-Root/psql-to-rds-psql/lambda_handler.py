# -*- coding: utf-8 -*-

import base64
import os
import pickle
import random
import string
from datetime import datetime

import boto3
from sqlalchemy import (
    Column, Index, ForeignKey,
    String, Integer, DateTime,
    select, insert,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def is_lambda_runtime():
    return "AWS_LAMBDA_FUNCTION_NAME" in os.environ


aws_profile_name = None if is_lambda_runtime() else "eq_sanhe"

ses = boto3.session.Session(profile_name=aws_profile_name)
cf = ses.resource("cloudformation")

if is_lambda_runtime():
    project_name = os.environ["PROJECT_NAME"]
    db_username = os.environ["DB_USERNAME"]
    db_password = os.environ["DB_PASSWORD"]
else:
    from config import Params

    project_name = Params.project_name
    db_username = Params.db_username
    db_password = Params.db_password

stack = cf.Stack(project_name)

outputs_dict = {
    output_dict["OutputKey"]: output_dict["OutputValue"]
    for output_dict in stack.outputs
}

db_endpoint = outputs_dict["DBEndpoint"]
db_port = outputs_dict["DBPort"]

conn_str = "postgresql+psycopg2://{}:{}@{}:{}/postgres".format(
    db_username, db_password, db_endpoint, db_port
)
engine = create_engine(conn_str)

Base = declarative_base()


# ---
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(Integer, ForeignKey("users.user_id"))
    create_time = Column(DateTime)


Index("idx_post_create_time", Post.create_time)


class Comment(Base):
    __tablename__ = "comments"

    thread_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    content = Column(String)
    create_time = Column(DateTime)


Index("idx_comment_post_id", Comment.post_id)
Index("idx_comment_create_time", Comment.create_time)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# ses = Session()

if os.path.exists("sqls.txt"):
    os.remove("sqls.txt")


def rand_str(length):
    return "".join([
        random.choice(string.ascii_lowercase)
        for _ in range(length)
    ])


def dump_stmt(f, stmt):
    f.write(
        base64.b64encode(pickle.dumps(stmt)).decode("utf8") + "\n"
    )


def clear_all_data():
    orm_class_list = [
        User, Post, Comment
    ]
    with engine.connect() as conn:
        for orm_class in orm_class_list:
            conn.execute(orm_class.__table__.delete())


class Behavior:
    n_post_per_page = 10

    def list_some_post(self):
        select(post)


def create_many_sql_stmt():
    n_user = 10
    n_post_per_user_lower = 1
    n_post_per_user_upper = 100
    n_comment_per_post_lower = 0
    n_comment_per_post_upper = 1000

    user_id_set = set()
    post_id_set = set()
    thread_id_set = set()

    with open("sqls.txt", "a") as f:
        for user_id in range(1, n_user + 1):
            stmt = insert(User.__table__).values(
                user_id=user_id, username=rand_str(10), password=rand_str(12)
            )
            dump_stmt(f, stmt)

        # post 1000
        for _ in range(1000):
            max_post_id = len(post_id_set)
            post_id = max_post_id + 1

            stmt = insert(Post.__table__).values(
                post_id=post_id,
                title=rand_str(random.randint(20, 50)),
                content=rand_str(random.randint(20, 1000)),
                author=random.randint(1, n_user),  # random user post this
                create_time=datetime.now(),
            )
            dump_stmt(f, stmt)
            post_id_set.add(post_id)
            print(stmt)
            # for


def execute_many_sql_stmt():
    with open("sqls.txt", "r") as f:
        with engine.connect().execution_options(autocommit=True) as conn:
            for line in f:
                stmt = pickle.loads(base64.b64decode(line.encode("utf-8")))
                conn.execute(stmt)


if __name__ == "__main__":
    clear_all_data()
    # create_many_sql_stmt()
    # execute_many_sql_stmt()
