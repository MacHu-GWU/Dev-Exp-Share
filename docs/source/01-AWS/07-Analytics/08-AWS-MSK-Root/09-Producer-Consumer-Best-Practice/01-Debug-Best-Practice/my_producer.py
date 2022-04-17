# -*- coding: utf-8 -*-

import time
import boto3
from kafka import KafkaProducer

# ------------------------------------------------------------------------------
# Define your Configuration here
# ------------------------------------------------------------------------------
class Config:
    aws_region = "us-east-1"
    cluster_name = "iam-access-test2"
    topic_name = "DatabaseStream"


cfg = Config()

# ------------------------------------------------------------------------------
# Resolve Connection Information
# ------------------------------------------------------------------------------
boto_ses = boto3.session.Session(region_name=cfg.aws_region)
msk_client = boto_ses.client("kafka")

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_clusters
res = msk_client.list_clusters(ClusterNameFilter=cfg.cluster_name)
cluster_arn = res["ClusterInfoList"][0]["ClusterArn"]

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_bootstrap_brokers
res = msk_client.get_bootstrap_brokers(ClusterArn=cluster_arn)
bootstrap_broker_list = res["BootstrapBrokerStringTls"].split(",")

# ------------------------------------------------------------------------------
# Create Producer Client
# ------------------------------------------------------------------------------
# Ref: https://kafka-python.readthedocs.io/en/master/_modules/kafka/producer/kafka.html
producer = KafkaProducer(
    bootstrap_servers=bootstrap_broker_list,
    client_id="my-producer-instance-001",
    security_protocol="SSL",
    linger_ms=1000,
)
# if authentication passed, print this
print("authentication passed!")
# if authentication failed, (username, password error), will raise this error
# kafka.errors.NoBrokersAvailable: NoBrokersAvailable

# ------------------------------------------------------------------------------
# Start producing data
# ------------------------------------------------------------------------------
n_message = 100
for ith in range(1, 1+n_message):
    time.sleep(0.1)
    message = f"this is {ith} message".encode("utf-8")
    producer.send(cfg.topic_name, value=message)
