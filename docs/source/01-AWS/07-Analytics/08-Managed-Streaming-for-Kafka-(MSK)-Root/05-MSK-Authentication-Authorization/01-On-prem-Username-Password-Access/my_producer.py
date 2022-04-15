# -*- coding: utf-8 -*-

import pysecret
from kafka import KafkaProducer

aws_region= "us-east-1"
bootstrap_servers_sasl = "b-3.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096,b-2.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096,b-1.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096".split(",")
topic_name = "DatabaseStream"
secret_id = "AmazonMSK_sanhe-username-password-test/alice"
aws = pysecret.AWSSecret(region_name=aws_region)
username = aws.get_secret_value(secret_id=secret_id, json_path="username")
password = aws.get_secret_value(secret_id=secret_id, json_path="password")
print(password)
# Ref: https://kafka-python.readthedocs.io/en/master/_modules/kafka/producer/kafka.html
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers_sasl,
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
future = producer.send(topic_name, key=message, value=message)
producer.flush()
