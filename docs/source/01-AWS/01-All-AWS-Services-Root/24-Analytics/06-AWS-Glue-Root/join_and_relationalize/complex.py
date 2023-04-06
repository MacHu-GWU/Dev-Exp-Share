# -*- coding: utf-8 -*-

"""

"""

import boto3
import awswrangler as wr
import pandas as pd

aws_profile = "eq_sanhe"
aws_region = "us-east-1"
bucket_name = "eq-sanhe-for-everything"

boto3.setup_default_session(profile_name="eq_sanhe", region_name="us-east-1")

# df = pd.DataFrame(
#     [
#         dict(id=1, name="Alice"),
#         dict(id=2, name="Bob"),
#         dict(id=3, name="Cathy"),
#     ],
#     columns="id,name".split(",")
# )
# wr.s3.copy_objects(
#     paths=[
#         "s3://awsglue-datasets/examples/us-legislators/all/"
#     ]
# )


# df = wr.s3.read_csv(path=f"s3://{bucket_name}/data/aws-glue-test/before/test.csv")
# print(df)

ab = {
  "identifiers": [
    {
      "scheme": "wikidata",
      "identifier": "Q3682992"
    }
  ],
  "other_names": [
    {
      "lang": "en",
      "note": "multilingual",
      "name": "At-large"
    },
    {
      "lang": "it",
      "note": "multilingual",
      "name": "Collegio unico"
    },
    {
      "lang": "fr",
      "note": "multilingual",
      "name": "scrutin plurinominal"
    },
    {
      "lang": "zh",
      "note": "multilingual",
      "name": "溫市的全體選民選出"
    },
    {
      "lang": "it",
      "note": "multilingual",
      "name": "Collegio unico nazionale"
    }
  ],
  "id": "party/al",
  "classification": "party",
  "name": "AL"
}