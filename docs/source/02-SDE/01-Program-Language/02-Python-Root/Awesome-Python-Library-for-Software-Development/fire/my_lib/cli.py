# -*- coding: utf-8 -*-

from .ec2 import EC2
from .s3 import S3

class Command:
    def __init__(self):
        self.ec2 = EC2()
        self.s3 = S3()
