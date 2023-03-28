# -*- coding: utf-8 -*-

"""
User
Video




user like a video
user follow another user


given user, return list of video he liked
given a video, return list of user who liked this video

given user, return list of user he followed
given user, return list of follower user

"""

import os
import typing
from datetime import datetime

import pynamodb
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.connection import Connection
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection, IncludeProjection
from pynamodb.models import Model

os.environ["AWS_PROFILE"] = "eq_sanhe"

connection = Connection()


class ExtendedModel(Model):
    @classmethod
    def key_attrs(cls) -> typing.List[str]:
        l = [cls._hash_keyname]
        if cls._range_keyname:
            l.append(cls._range_keyname)
        return l


class UserModel(ExtendedModel):
    """
    A DynamoDB User
    """
    N_USER_COUNTER = 0

    class Meta:
        table_name = "tiktok-user"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    user_id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()


class AuthorVideoIndex(GlobalSecondaryIndex):
    class Meta:
        index = "tiktok-author-video-index"
        projection = IncludeProjection(non_attr_keys=["video_id", ])

    author_id = UnicodeAttribute(hash_key=True)
    create_time = UnicodeAttribute(range_key=True)


class VideoModel(ExtendedModel):
    N_VIDEO_COUNTER = 0

    class Meta:
        table_name = "tiktok-video"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    video_id = UnicodeAttribute(hash_key=True)
    create_time = UnicodeAttribute(range_key=True, default=lambda: str(datetime.now()))
    title = UnicodeAttribute()
    author_id = UnicodeAttribute()
    likes = NumberAttribute(default=0)

    author_video_index = AuthorVideoIndex()


class VideoLikedByUserIndex(GlobalSecondaryIndex):
    class Meta:
        index = "tiktok-video-liked-by-user-index"
        projection = KeysOnlyProjection()

    video_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)


class UserLikeVideoModel(ExtendedModel):
    class Meta:
        table_name = "tiktok-user-like-video"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    user_id = UnicodeAttribute(hash_key=True)
    video_id = UnicodeAttribute(range_key=True)

    video_liked_by_user_iindex = VideoLikedByUserIndex()


model_list: typing.List[ExtendedModel] = [
    UserModel,
    VideoModel,
    UserLikeVideoModel,
]

for model in model_list:
    model.create_table(wait=True)


# class ItemOrderIndex(GlobalSecondaryIndex):
#     class Meta:
#         index = "many-to-many-department-item-and-order-index-3"
#         projection = KeysOnlyProjection
#
#     item_id = UnicodeAttribute(hash_key=True)
#     order_id = UnicodeAttribute(range_key=True)
#
#
# class OrderAndItem(Model):
#     class Meta:
#         table_name = "many-to-many-order-and-item-3"
#         region = "us-east-1"
#         billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE
#
#     order_id = UnicodeAttribute(hash_key=True)
#     item_id = UnicodeAttribute(range_key=True)
#
#     item_order_index = ItemOrderIndex()
#
#     @classmethod
#     def create_order(cls, order_id, item_id_list):
#         with OrderAndItem.batch_write() as batch:
#             for item_id in item_id_list:
#                 batch.save(cls(order_id=order_id, item_id=item_id))


class Api:
    @classmethod
    def create_new_user(cls, username):
        user = UserModel(
            user_id="u-{}".format(UserModel.N_USER_COUNTER + 1),
            username=username,
        )
        user.save(condition=UserModel.user_id.does_not_exist())
        UserModel.N_USER_COUNTER += 1

    @classmethod
    def upload_new_video(cls, user_id, title):
        video = VideoModel(
            video_id="v-{}".format(VideoModel.N_VIDEO_COUNTER + 1),
            title=title,
            author_id=user_id,
        )
        video.save(condition=VideoModel.video_id.does_not_exist())
        VideoModel.N_VIDEO_COUNTER += 1

    @classmethod
    def user_like_a_video(cls, user_id, video_id):
        ulv = UserLikeVideoModel(user_id=user_id, video_id=video_id)
        ulv.save()

    @classmethod
    def user_unlike_a_video(cls, user_id, video_id):
        ulv = UserLikeVideoModel(user_id=user_id, video_id=video_id)
        ulv.delete()


class BQuery:
    @classmethod
    def count_users(cls) -> int:
        return UserModel.count()

    @classmethod
    def list_user_following(cls, user_id) -> typing.Iterable[str]:
        """
        Given an user_id representing Mr X, returns list of user_id Mr X is following
        """

    @classmethod
    def count_user_following(cls, user_id) -> int:
        """
        Given an user_id representing Mr X, return the number of user Mr X is following
        """

    @classmethod
    def list_user_follower(cls, user_id) -> typing.Iterable[str]:
        """
        Given an user_id representing Mr X, returns list of user_id who is following Mr X
        """

    @classmethod
    def count_user_follower(cls, user_id) -> int:
        """
        Given an user_id representing Mr X, return the number of user who is following Mr X
        """

    @classmethod
    def list_user_liked(cls, user_id) -> typing.Iterable[str]:
        """
        Given an user_id representing Mr X, returns list of video_id Mr X liked
        """

    @classmethod
    def count_user_liked(cls, user_id) -> int:
        """
        Given an user_id representing Mr X, returns number of video Mr X liked
        """

    @classmethod
    def list_user_upload(cls, user_id) -> typing.Iterable[str]:
        """
        Given an user_id representing Mr X, returns list of video_id Mr X uploaded
        """

    @classmethod
    def count_user_upload(cls, user_id) -> int:
        """
        Given an user_id representing Mr X, returns number of video_id Mr X uploaded
        """

    @classmethod
    def describe_video_uploader(cls, video) -> str:
        """
        Given a video_id, returns the user_id of it's uploader
        """

    @classmethod
    def count_video_likes(cls, video_id) -> int:
        """
        Given a video_id, returns the number of user who like this video
        """

    @classmethod
    def is_user_like_this_video(cls, user_id, video_id) -> bool:
        """
        Given a user_id and video_id, return boolean value to indicate that
        whether the user like the video
        """

    @classmethod
    def list_video_comments(cls, video_id) -> list:
        pass


def create_dummy_data():
    # create users
    user_list = ["Alice", "Bob", "Cathy"]
    for username in user_list:
        Api.create_new_user(username)

    # upload videos
    video_list = [
        ("u-1", "the v-1"),
        ("u-2", "the v-2"),
        ("u-2", "the v-3"),
        ("u-3", "the v-4"),
        ("u-3", "the v-5"),
        ("u-3", "the v-6"),
    ]

    for user_id, title in video_list:
        Api.upload_new_video(user_id=user_id, title=title)

    # users like videos
    user_like_video = [
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 1),
        (2, 5),
        (3, 1),
        (3, 2),
        (3, 3),
    ]
    for user_id, video_id in user_like_video:
        Api.user_like_a_video(user_id=user_id, video_id=video_id)


def empty_all_table():
    # pass
    for model in model_list:
        with model.batch_write() as batch:
            for item in model.scan(attributes_to_get=model.key_attrs()):
                batch.delete(item)


def delete_all_table():
    for model in model_list:
        model.delete_table()


if __name__ == "__main__":
    empty_all_table()
    create_dummy_data()
    # delete_all_table()
