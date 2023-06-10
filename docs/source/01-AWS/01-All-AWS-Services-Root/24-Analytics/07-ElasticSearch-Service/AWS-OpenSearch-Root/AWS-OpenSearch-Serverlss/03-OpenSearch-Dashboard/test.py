import boto3
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection


client = boto3.client('opensearchserverless')
service = 'aoss'
region = 'us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

host = "f5sy8qv0vib1x2bsncz3.us-east-1.aoss.amazonaws.com"
oss = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300
)
# It can take up to a minute for data access rules to be enforced
# time.sleep(45)
# res = oss.ping()
# print(res)

query = {
  'size': 5,
  'query': {
    'match_all': {}
  }
}



index_name = "opensearch_dashboards_sample_data_ecommerce"
res = oss.indices.exists(index=index_name)
# res = oss.cat.indices(format="json")
# res = oss.cluster.state()
# res = oss.indices.exists(index=index_name)

# res = oss.search(
#     body = query,
#     index = index_name
# )

rprint(res)
print(type(res))
