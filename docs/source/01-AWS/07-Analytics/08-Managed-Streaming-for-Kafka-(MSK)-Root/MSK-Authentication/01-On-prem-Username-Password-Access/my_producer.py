# -*- coding: utf-8 -*-

from kafka import KafkaProducer
from kafka.errors import KafkaError

bootstrap_servers_sasl = "b-3.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096,b-2.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096,b-1.on-prem-user-pass-con.ey78pz.c24.kafka.us-east-1.amazonaws.com:9096".split(",")
username = "alice"
password = "FYd^u2gdYg5#"
topic_name = "DatabaseStream"

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers_sasl,
    sasl_plain_username=username,
    sasl_plain_password=password,
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
)

print("authentication passed!")

message = "hello kafka".encode("utf-8")
future = producer.send(topic_name, key=message, value=message)
producer.flush()
