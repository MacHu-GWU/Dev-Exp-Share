# -*- coding: utf-8 -*-

import os

import boto3
import pynamodb
import pynamodb.exceptions as exc
from pynamodb.attributes import (
    UnicodeAttribute, BooleanAttribute, ListAttribute, NumberAttribute,
)
from pynamodb.models import Model


# --- Resovle Constant Value ---
def is_lambda_runtime():
    return "AWS_LAMBDA_FUNCTION_NAME" in os.environ


if is_lambda_runtime():
    aws_profile = None
else:
    aws_profile = "eq_sanhe"
    os.environ["AWS_PROFILE"] = "eq_sanhe"

ses = boto3.session.Session(profile_name=aws_profile)
sqs = boto3.resource("sqs")
q_url = "https://sqs.us-east-1.amazonaws.com/110330507156/poc-fifo-q.fifo"
q = sqs.Queue(q_url)

q_url = "https://sqs.us-east-1.amazonaws.com/110330507156/poc-fifo-q-dlq.fifo"
dlq = sqs.Queue(q_url)


# --- Define DynamoDB Model ---
class SQSTrackerModel(Model):
    """
    A DynamoDB User
    """

    class Meta:
        table_name = "poc-fifo-q-sqs-tracker"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    id = UnicodeAttribute(hash_key=True)
    flag = BooleanAttribute()


class OutputModel(Model):
    """
    This model can store up to 82500 member. For example this object is appr
    256KB in dynamodb:

    {
        gid: "1",
        processed: [1, 2, ..., 82500]
    }
    """

    class Meta:
        table_name = "poc-fifo-q-output"
        region = "us-east-1"
        billing_mode = pynamodb.models.PAY_PER_REQUEST_BILLING_MODE

    gid = UnicodeAttribute(hash_key=True)
    processed = ListAttribute(of=NumberAttribute, default=list)


if not is_lambda_runtime():
    SQSTrackerModel.create_table(wait=True)
    OutputModel.create_table(wait=True)


def debug_consumer():
    attempt_id = "7b3a46183cfedf9a72d87ca5cff1ec8b"
    res = q.receive_messages(
        MaxNumberOfMessages=1,
        AttributeNames=["All", ],
        ReceiveRequestAttemptId=attempt_id,
    )
    for msg in res:
        print(msg.message_id)
        print(msg.body)
        print(msg.md5_of_body)
        print(msg.receipt_handle)
        print(msg.attributes)


def debug_output():
    def strict_ascend(l):
        previous = 0
        for i in l:
            if i > previous:
                previous = i
                continue
            else:
                raise ValueError

    def validate_output(gid, processed):
        if len(processed) != len(set(processed)):
            print(f"{gid}: duplicate item found!")
        else:
            print(f"{gid}: no duplicate item.")
        try:
            strict_ascend(processed)
            print(f"{gid}: is strictly in order.")
        except ValueError:
            print(f"{gid}: is not in order!")

    total = 0
    for o in OutputModel.scan():
        print(o.gid, o.processed)
        validate_output(o.gid, o.processed)
        total += len(o.processed)

    print(f"total processed item = {total}")


def clear_q_and_db():
    """
    purge all message in all q, clear all data in dynamodb. reset test
    environment.
    """
    q.purge()
    dlq.purge()

    for model in [SQSTrackerModel, OutputModel]:
        with model.batch_write() as batch:
            item_list = list(model.scan())
            for item in item_list:
                batch.delete(item)


def main_good(event, context):
    for record_dct in event["Records"]:
        message_id = record_dct["messageId"]

        # make sure this message is never successfully consumed before
        try:
            q_tracker = SQSTrackerModel.get(message_id)
            if q_tracker.flag:
                continue  # skip this record
        except SQSTrackerModel.DoesNotExist:
            pass
        except Exception as e:
            # since if one failed, all message will go back to queue anyway
            # we should stop earlier
            raise e

        # consume this message
        gid, nth = record_dct["body"].split("-")
        nth: int = int(nth)

        try:
            OutputModel(gid=gid).update(
                actions=[
                    OutputModel.processed.set(OutputModel.processed.append([nth, ]))
                ],
                condition=OutputModel.gid.exists(),
            )
        except exc.UpdateError as e:
            if "The conditional request failed" in str(e):
                OutputModel(gid=gid, processed=[nth, ]).save(
                    condition=OutputModel.gid.does_not_exist(),
                )
            else:
                raise e
        except Exception as e:
            raise e

        # mark this message "processed" in tracker
        SQSTrackerModel(id=message_id, flag=True).save()


def main_with_error(event, context):
    for record_dct in event["Records"]:
        message_id = record_dct["messageId"]

        # make sure this message is never successfully consumed before
        try:
            q_tracker = SQSTrackerModel.get(message_id)
            if q_tracker.flag:
                continue  # skip this record
        except SQSTrackerModel.DoesNotExist:
            pass
        except Exception as e:
            # since if one failed, all message will go back to queue anyway
            # we should stop earlier
            raise e

        # consume this message
        gid, nth = record_dct["body"].split("-")
        nth: int = int(nth)

        if gid == "g1" and nth == 11:  # g1 should only good up to some value before 11, could be random value from 1 - 11
            raise ValueError

        try:
            OutputModel(gid=gid).update(
                actions=[
                    OutputModel.processed.set(OutputModel.processed.append([nth, ]))
                ],
                condition=OutputModel.gid.exists(),
            )
        except exc.UpdateError as e:
            if "The conditional request failed" in str(e):
                OutputModel(gid=gid, processed=[nth, ]).save(
                    condition=OutputModel.gid.does_not_exist(),
                )
            else:
                raise e
        except Exception as e:
            raise e

        # mark this message "processed" in tracker
        SQSTrackerModel(id=message_id, flag=True).save()


main = main_with_error

if __name__ == "__main__":
    pass
    # debug_consumer()
    # debug_output()
    # clear_q_and_db()
