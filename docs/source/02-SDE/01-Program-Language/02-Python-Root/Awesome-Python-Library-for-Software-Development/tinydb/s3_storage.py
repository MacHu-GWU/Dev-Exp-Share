# -*- coding: utf-8 -*-

import json
import tinydb
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager


class S3Storage(tinydb.Storage):
    def __init__(
        self,
        s3path: S3Path,
        bsm: BotoSesManager,
    ):
        self.s3path = s3path
        self.bsm = bsm

    def read(self):
        try:
            return json.loads(self.s3path.read_text(bsm=bsm))
        except Exception as e:
            if "does not exist" in str(e):
                self.write({})
            else:
                raise e

    def write(self, data):
        self.s3path.write_text(
            json.dumps(data, indent=4),
            content_type="application/json",
            bsm=self.bsm,
        )


bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)
bucket = f"{bsm.aws_account_id}-{bsm.aws_region}-data"
s3path = S3Path(f"s3://{bucket}/projects/tinydb/db.json")
print(s3path.console_url)
s3path.delete()

with tinydb.TinyDB(
    s3path=s3path,
    bsm=bsm,
    storage=S3Storage,
) as db:
    t_user = db.table("users")
    t_user.insert({"name": "John", "age": 123})

    User = tinydb.Query()
    print(t_user.search(User.name == "John"))
