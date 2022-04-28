# -*- coding: utf-8 -*-

import boto3
import pysecret
from kafka import KafkaProducer

# ==============================================================================
# Define your Configuration here
# ------------------------------------------------------------------------------
class Config:
    aws_region = "us-east-1"
    cluster_name = "on-prem-user-pass-conn-test1"
    secret_id = "AmazonMSK_sanhe-username-password-test/alice"
    topic_name = "DatabaseStream"
    public_access = False


cfg = Config()
# ==============================================================================

boto_ses = boto3.session.Session(region_name=cfg.aws_region)
msk_client = boto_ses.client("kafka")

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_clusters
res = msk_client.list_clusters(ClusterNameFilter=cfg.cluster_name)
cluster_arn = res["ClusterInfoList"][0]["ClusterArn"]

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_bootstrap_brokers
res = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
if cfg.public_access:
    bootstrap_broker_list = res["BootstrapBrokerStringPublicSaslScram"].split(",")
else:
    bootstrap_broker_list = res["BootstrapBrokerStringSaslScram"].split(",")

# Ref: https://github.com/MacHu-GWU/pysecret-project
aws = pysecret.AWSSecret(region_name=cfg.aws_region)
username = aws.get_secret_value(secret_id=cfg.secret_id, json_path="username")
password = aws.get_secret_value(secret_id=cfg.secret_id, json_path="password")

# Ref: https://kafka-python.readthedocs.io/en/master/_modules/kafka/producer/kafka.html
producer = KafkaProducer(
    bootstrap_servers=bootstrap_broker_list,
    sasl_plain_username=username,
    sasl_plain_password=password,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
)
# if authentication passed, print this
print("authentication passed!")
# if authentication failed, (username, password error), will raise this error
# kafka.errors.NoBrokersAvailable: NoBrokersAvailable

message = "hello kafka".encode("utf-8")
future = producer.send(cfg.topic_name, key=message, value=message)
producer.flush()
