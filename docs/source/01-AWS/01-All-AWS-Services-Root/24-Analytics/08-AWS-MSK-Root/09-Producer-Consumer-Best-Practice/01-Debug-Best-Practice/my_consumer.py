# -*- coding: utf-8 -*-

import time
import boto3
from kafka import KafkaConsumer

# ------------------------------------------------------------------------------
# Define your Configuration here
# ------------------------------------------------------------------------------
class Config:
    aws_region= "us-east-1"
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
# Create Consumer Client
# ------------------------------------------------------------------------------
# Ref: https://kafka-python.readthedocs.io/en/master/_modules/kafka/consumer/group.html
consumer = KafkaConsumer(
    cfg.topic_name,
    group_id="group1",
    bootstrap_servers=bootstrap_broker_list,
    security_protocol="SSL",
    fetch_min_bytes=16384,
    fetch_max_wait_ms=1000,
)
# # if authentication failed, (username, password error), will raise this error
# # kafka.errors.NoBrokersAvailable: NoBrokersAvailable
print("authentication passed!")

# ------------------------------------------------------------------------------
# Start consuming data
# ------------------------------------------------------------------------------
st = time.time()
for message in consumer:  # this is a endless for loop
    elapse = time.time() - st
    print(f"--- next iteration, elapsed {elapse} ---")
    print(type(message), message)
consumer.commit()