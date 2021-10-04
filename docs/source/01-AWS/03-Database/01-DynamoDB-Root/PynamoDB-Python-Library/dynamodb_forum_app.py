# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, LocalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute

# os.environ["AWS_DEFAULT_PROFILE"] = "skymap_sandbox"


class UserModel(Model):
    class Meta:
        table_name = "learn-dynamodb-users"
        region = "us-east-1"
        read_capacity_units = 5
        write_capacity_units = 5

    username = UnicodeAttribute(hash_key=True)
    firstname = UnicodeAttribute(null=True)
    lastname = UnicodeAttribute(null=True)


UserModel.create_table(read_capacity_units=5, write_capacity_units=5)



class BoardNameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "posts-board_name-last_update"
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    board_name = UnicodeAttribute(hash_key=True)
    last_update = UnicodeAttribute(range_key=True)


class PostModel(Model):
    """
    1. 列出某板块的所有 Post, 按照 last_update (最后回复) 倒序排列, 每页显示 10 个
    2. 根据 post_id, 获取 Post 信息.
    3. 查找某个作者的所有帖子.
    """

    class Meta:
        table_name = "learn-dynamodb-posts"
        region = "us-east-1"
        read_capacity_units = 5
        write_capacity_units = 5

    post_id = UnicodeAttribute(hash_key=True)
    board_name_index = BoardNameIndex()
    board_name = UnicodeAttribute()
    last_update = UnicodeAttribute(range_key=True)
    create_time = UnicodeAttribute()
    author_username = UnicodeAttribute()
    title = UnicodeAttribute()

PostModel.create_table(read_capacity_units=1, write_capacity_units=1)


class TagModel(Model):
    """
    1. 列出所有包含某个标签, 或是包含多个标签的 Post
    """

    class Meta:
        table_name = "learn-dynamodb-tags"
        region = "us-east-1"
        read_capacity_units = 5
        write_capacity_units = 5

    tag_name = UnicodeAttribute(hash_key=True)
    post_id = UnicodeAttribute(range_key=True)

TagModel.create_table(read_capacity_units=1, write_capacity_units=1)


def delete_all(model):
    with model.batch_write() as batch:
        item_list = list(model.scan())
        for item in item_list:
            batch.delete(item)


# reset table first

def reset():
    delete_all(UserModel)
    delete_all(PostModel)
    delete_all(TagModel)


def create_test_data():
    tag_name_list = ["Python", "Java", "Go"]
    board_name_list = [tag + " board" for tag in tag_name_list]

    user_alice = UserModel(username="Alice")
    user_alice.save()

    post_data = list()
    tag_data = list()
    for pid in range(1, 1 + 10):
        utcnow = str(datetime.utcnow())
        post = PostModel(
            post_id="pid_%s" % str(pid).zfill(10),
            board_name=random.choice(board_name_list),
            last_update=utcnow,
            create_time=utcnow,
            author_username=user_alice.username,
            title="Alice's %s th post" % pid
        )
        post_data.append(post)
        for tag_name in random.sample(tag_name_list, random.randint(1, 3)):
            tag = TagModel(tag_name=tag_name, post_id=post.post_id)
            tag_data.append(tag)

    with PostModel.batch_write() as batch:
        for post in post_data:
            batch.save(post)

    with TagModel.batch_write() as batch:
        for tag in tag_data:
            batch.save(tag)

reset()
create_test_data()

# 列出某个板块的所有帖子
n_post_each_page = 10
for post in PostModel.board_name_index.query(hash_key="Python board", scan_index_forward=False, limit=n_post_each_page):
    print(post)

# 统计某个板块有多少个帖子
n_post_on_python_board = PostModel.board_name_index.count(hash_key="Python board")
print(n_post_on_python_board)

# 列出所有包含 Python 标签的帖子
for tag in TagModel.query(hash_key="Python", scan_index_forward=False):
    print(tag)
