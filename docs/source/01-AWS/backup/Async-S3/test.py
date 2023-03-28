import time
import json
import boto3
import asyncio
import aioboto3
from io import BytesIO


def generate_content():
    data = [{"id": 1, "name": "Alice"},] * 100000
    text = json.dumps(data)
    blob = text.encode("utf-8")
    return blob

aws_profile = "sanhe"
aioboto3.setup_default_session(profile_name=aws_profile)
bucket_name = "pyrabbit"
blob = generate_content()


ses = boto3.Session(profile_name=aws_profile)

def generate_buffer(blob):
    buffer = BytesIO(blob)
    return buffer

def normal_version():
    s3 = ses.client("s3")
    result1 = s3.upload_fileobj(BytesIO(blob), bucket_name, "a.json")
    result2 = s3.upload_fileobj(BytesIO(blob), bucket_name, "b.json")
    result3 = s3.upload_fileobj(BytesIO(blob), bucket_name, "c.json")


async def async_version():
    async with aioboto3.client("s3") as s3:
        result1 = await s3.upload_fileobj(BytesIO(blob), bucket_name, "a.json")
        result2 = await s3.upload_fileobj(BytesIO(blob), bucket_name, "b.json")
        result3 = await s3.upload_fileobj(BytesIO(blob), bucket_name, "c.json")
        print(result1)
        print(result2)
        print(result3)


st = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(async_version())
# normal_version()
elapse = time.time() - st
print("%.6f" % elapse)
