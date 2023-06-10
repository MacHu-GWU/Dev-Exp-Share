# -*- coding: utf-8 -*-

"""
Maintain an importable OpenSearch client connection to use.
"""

import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection

# from .boto_ses import bsm


def create_connection(
    boto_ses: boto3.session.Session,
    aws_region: str,
    es_endpoint: str,
    test: bool = True,
) -> OpenSearch:
    """
    Create an AWS Opensearch connection to a domain.
    """
    if es_endpoint.startswith("https://"):
        es_endpoint = es_endpoint.replace("https://", "", 1)
    print(es_endpoint)
    credentials = boto_ses.get_credentials()
    aws_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        aws_region,
        "aoss",
        session_token=credentials.token,
    )
    es = OpenSearch(
        hosts=[{"host": es_endpoint, "port": 443}],
        # hosts=[f"{es_endpoint}:443"],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    if test:
        es.info()
    return es


# oss = open search service
oss = create_connection(
    # boto_ses=bsm.boto_ses,
    boto_ses=boto3.session.Session(profile_name="aws_data_lab_sanhe_us_east_1"),
    aws_region="us-east-1",
    es_endpoint="https://f5sy8qv0vib1x2bsncz3.us-east-1.aoss.amazonaws.com",
    test=True,
)
