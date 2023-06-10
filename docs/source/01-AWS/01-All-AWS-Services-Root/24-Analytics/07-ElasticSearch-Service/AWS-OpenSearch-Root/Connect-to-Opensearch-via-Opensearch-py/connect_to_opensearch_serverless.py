# -*- coding: utf-8 -*-

"""
Sample code to create a connection to an opensearch domain.
"""

import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection


def create_connection(
    boto_ses: boto3.session.Session,
    aws_region: str,
    oss_endpoint: str,
    test: bool = True,
) -> OpenSearch:
    """
    Create an AWS Opensearch connection to a domain.

    Reference:

    - https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-sdk.html
    """
    # ensure that the endpoint doesn't have the ``https://`` part
    if oss_endpoint.startswith("https://"):
        oss_endpoint = oss_endpoint.replace("https://", "", 1)

    credentials = boto_ses.get_credentials()
    aws_auth = AWS4Auth(
        # Note, the first four are positioning argument, you cannot use keyword argument
        credentials.access_key,
        credentials.secret_key,
        aws_region,  # region
        "aoss",  # service name is aoss for opensearch serverless
        session_token=credentials.token,
    )
    oss = OpenSearch(
        hosts=[{"host": oss_endpoint, "port": 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    if test:
        oss.cat.indices(format="json")
    return oss


# oss = open search service
oss = create_connection(
    boto_ses=boto3.session.Session(profile_name="my_profile"),
    aws_region="us-east-1",
    oss_endpoint="https://1a2b3c4d.us-east-1.aoss.amazonaws.com",
    test=True,
)
res = oss.cat.indices(format="json")
print(res)
