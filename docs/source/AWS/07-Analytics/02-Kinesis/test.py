import boto3
import json

ses = boto3.Session(profile_name="identitysandbox.gov")
kin = ses.client("kinesis")
stream_name = "sanh-test"
kin.put_records(
    Records=[
        {
            "Data": json.dumps({"id": 1, "name": "Alice"}).encode("utf-8"),
            "PartitionKey": "id",
        },
    ] * 100,
    StreamName=stream_name,
)