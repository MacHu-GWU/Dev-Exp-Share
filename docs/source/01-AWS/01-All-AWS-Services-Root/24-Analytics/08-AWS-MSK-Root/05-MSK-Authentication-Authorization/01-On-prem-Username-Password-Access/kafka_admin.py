#!/bin/bash

import json
import boto3
import shutil
import subprocess
from pathlib import Path
from typing import List


# ------------------------------------------------------------------------------
# Update config values accordingly

class Config:
    """
    :param kafka_scala_version, kafka_version: You can find the recommended value
        for ``kafka_scala_version`` and ``kafka_version`` at
        https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html
    :param cluster_name: put your MSK cluster name here, the short one, not the ARN
    :param topic_name: the Kafka topic you want to create for testing
    """
    kafka_scala_version = "2.12"
    kafka_version = "2.6.2"
    cluster_name = "on-prem-user-pass-conn-test1"
    topic_name = "DatabaseStream"


# ------------------------------------------------------------------------------


kakfa_tar_filename = f"kafka_{Config.kafka_scala_version}-{Config.kafka_version}"
kafka_tar_download_url = f"https://archive.apache.org/dist/kafka/{Config.kafka_version}/{kakfa_tar_filename}.tgz"

dir_here = Path(__file__).absolute().parent
p_kafka_tar_file = Path(dir_here, f"{kakfa_tar_filename}.tgz")
dir_kafka = Path(dir_here, kakfa_tar_filename)
dir_kafka_bin = Path(dir_kafka, "bin")

print(f"- current working directory: {dir_here}")
print(f"- kakfa download url: {kafka_tar_download_url}")
print(f"- kakfa tar file: {p_kafka_tar_file}")
print(f"- kafka directory: {dir_kafka}")

p_bin_connect_distributed = Path(dir_kafka_bin, "connect-distributed.sh")
p_bin_connect_mirror_maker = Path(dir_kafka_bin, "connect-mirror-maker.sh")
p_bin_connect_standalone = Path(dir_kafka_bin, "connect-standalone.sh")
p_bin_kafka_acls = Path(dir_kafka_bin, "kafka-acls.sh")
p_bin_kafka_broker_api_versions = Path(dir_kafka_bin, "kafka-broker-api-versions.sh")
p_bin_kafka_configs = Path(dir_kafka_bin, "kafka-configs.sh")
p_bin_kafka_console_consumer = Path(dir_kafka_bin, "kafka-console-consumer.sh")
p_bin_kafka_console_producer = Path(dir_kafka_bin, "kafka-console-producer.sh")
p_bin_kafka_consumer_groups = Path(dir_kafka_bin, "kafka-consumer-groups.sh")
p_bin_kafka_consumer_perf_test = Path(dir_kafka_bin, "kafka-consumer-perf-test.sh")
p_bin_kafka_delegation_tokens = Path(dir_kafka_bin, "kafka-delegation-tokens.sh")
p_bin_kafka_delete_records = Path(dir_kafka_bin, "kafka-delete-records.sh")
p_bin_kafka_dump_log = Path(dir_kafka_bin, "kafka-dump-log.sh")
p_bin_kafka_leader_election = Path(dir_kafka_bin, "kafka-leader-election.sh")
p_bin_kafka_log_dirs = Path(dir_kafka_bin, "kafka-log-dirs.sh")
p_bin_kafka_mirror_maker = Path(dir_kafka_bin, "kafka-mirror-maker.sh")
p_bin_kafka_preferred_replica_election = Path(dir_kafka_bin, "kafka-preferred-replica-election.sh")
p_bin_kafka_producer_perf_test = Path(dir_kafka_bin, "kafka-producer-perf-test.sh")
p_bin_kafka_reassign_partitions = Path(dir_kafka_bin, "kafka-reassign-partitions.sh")
p_bin_kafka_replica_verification = Path(dir_kafka_bin, "kafka-replica-verification.sh")
p_bin_kafka_run_class = Path(dir_kafka_bin, "kafka-run-class.sh")
p_bin_kafka_server_start = Path(dir_kafka_bin, "kafka-server-start.sh")
p_bin_kafka_server_stop = Path(dir_kafka_bin, "kafka-server-stop.sh")
p_bin_kafka_streams_application_reset = Path(dir_kafka_bin, "kafka-streams-application-reset.sh")
p_bin_kafka_topics = Path(dir_kafka_bin, "kafka-topics.sh")
p_bin_kafka_verifiable_consumer = Path(dir_kafka_bin, "kafka-verifiable-consumer.sh")
p_bin_kafka_verifiable_producer = Path(dir_kafka_bin, "kafka-verifiable-producer.sh")
p_bin_trogdor = Path(dir_kafka_bin, "trogdor.sh")
p_bin_zookeeper_security_migration = Path(dir_kafka_bin, "zookeeper-security-migration.sh")
p_bin_zookeeper_server_start = Path(dir_kafka_bin, "zookeeper-server-start.sh")
p_bin_zookeeper_server_stop = Path(dir_kafka_bin, "zookeeper-server-stop.sh")
p_bin_zookeeper_shell = Path(dir_kafka_bin, "zookeeper-shell.sh")

boto_ses = boto3.session.Session()
aws_region = boto_ses.region_name

msk_client = boto_ses.client("kafka")
res = msk_client.list_clusters(ClusterNameFilter=Config.cluster_name)
cluster_arn = res["ClusterInfoList"][0]["ClusterArn"]


def s1_download_kafka_tar_file():
    """

    """
    if not p_kafka_tar_file.exists():
        subprocess.run(
            [
                "wget", kafka_tar_download_url, "-O", str(p_kafka_tar_file),
            ],
        )


def s2_extract_kafka():
    """

    """
    if not dir_kafka.exists():
        subprocess.run(
            [
                "tar", "-xzf", str(p_kafka_tar_file), "-C", str(dir_here),
            ],
        )


def s3_get_zookeeper_conn_str(
    aws_region: str,
    cluster_arn: str,
) -> str:
    output = subprocess.check_output(
        [
            "aws", "kafka", "describe-cluster",
            "--region", aws_region,
            "--cluster-arn", cluster_arn,
        ],
    ).decode("utf-8")
    zookeeper_conn_str = json.loads(output)["ClusterInfo"]["ZookeeperConnectString"]
    return zookeeper_conn_str


def s4_create_kafka_topic(topic_name: str, zookeeper_conn_str: str):
    """

    """
    output = subprocess.check_output(
        [
            str(p_bin_kafka_topics),
            "--list",
            "--zookeeper", zookeeper_conn_str
        ]
    ).decode("utf-8")
    existing_topic_list = [name.strip() for name in output.split("\n") if name.strip()]

    if topic_name not in existing_topic_list:
        print(f"Creating Kafka Topic: {topic_name!r}")
        subprocess.run(
            [
                str(p_bin_kafka_topics),
                "--create",
                "--zookeeper", zookeeper_conn_str,
                "--replication-factor", "3",
                "--partitions", "2",
                "--topic", topic_name,
            ]
        )
    else:
        print(f"Topic {topic_name!r} already exists!")


def create_client_properties_file():
    """
    Ref: https://docs.aws.amazon.com/msk/latest/developerguide/produce-consume.html
    """
    Path(dir_kafka_bin, "client.properties").write_text("security.protocol=PLAINTEXT")


def s5_get_bootstrap_broker_str(
    aws_region: str,
    cluster_arn: str,
) -> List[str]:
    """
    bootstrap broker (server) 是 Producer 和 Consumer 和 Kafka Cluster 之间建立连接的入口.
    首先要连接上其中任何一台 bootstrap server, 才能进而自动发现 Kafka 上所有的 broker 的
    网络连接信息. 最终 Producer 和 Consumer 发布和消费消息所连接的 Broker 跟 bootstrap broker
    可能相同, 也可能不同.
    """
    output = subprocess.check_output(
        [
            "aws", "kafka",
            "get-bootstrap-brokers",
            "--region", aws_region,
            "--cluster-arn", cluster_arn
        ]
    ).decode("utf-8")
    res = json.loads(output)
    print(json.dumps(res, indent=4))
    bootstrap_broker_str = json.loads(output)["BootstrapBrokerStringSaslScram"]
    return bootstrap_broker_str.split(",")

# s1_download_kafka_tar_file()
# s2_extract_kafka()
zookeeper_conn_str = s3_get_zookeeper_conn_str(aws_region=aws_region, cluster_arn=cluster_arn)
# s4_create_kafka_topic(topic_name=Config.topic_name, zookeeper_conn_str=zookeeper_conn_str)
botostrap_broker_str_list = s5_get_bootstrap_broker_str(aws_region=aws_region, cluster_arn=cluster_arn)
