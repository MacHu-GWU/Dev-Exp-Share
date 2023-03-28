# -*- coding: utf-8 -*-

import os
import rolex
from sfm.rnd import rand_hexstr
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

os.environ["AWS_DEFAULT_PROFILE"] = "eqtest"


class PostModel(Model):
    class Meta:
        table_name = "learn-data-pipline-dynamodb-to-s3-posts"
        region = "us-east-1"

    post_id = UnicodeAttribute(hash_key=True)
    create_time = UnicodeAttribute(range_key=True)


PostModel.create_table(read_capacity_units=25, write_capacity_units=25)


with PostModel.batch_write() as batch:
    n_article = 1000
    for id in range(1, 1+n_article):
        post = PostModel(
            post_id=rand_hexstr(32),
            create_time=str(rolex.rnd_datetime("2019-01-01", "2019-02-01")),
        )
        batch.save(post)


