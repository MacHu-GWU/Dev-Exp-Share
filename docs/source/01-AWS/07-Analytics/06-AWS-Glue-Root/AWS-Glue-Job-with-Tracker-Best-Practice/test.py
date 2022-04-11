import pynamodb
from pynamodb.models import Model
from pynamodb.connection import Connection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


# create boto3 dynamodb client connection with default AWS profile
connection = Connection()


# Create bank account data model
class Tracker(Model):
    class Meta:
        """
        declare metadata about the table
        """
        table_name = "learn_big_data_on_aws_glue_tracker"
        region = "us-east-2"

        # billing mode
        # doc: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html
        # pay as you go mode
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

        # provisioned mode
        # write_capacity_units = 10
        # read_capacity_units = 10

    # define attributes
    s3uri = UnicodeAttribute(hash_key=True)
    status = NumberAttribute(default=0)


# # Create dynamodb table if not exists, if already exists, this code won't do anything
Tracker.create_table(wait=True)