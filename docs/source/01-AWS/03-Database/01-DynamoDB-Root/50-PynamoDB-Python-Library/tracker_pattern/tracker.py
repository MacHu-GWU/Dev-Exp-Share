# -*- coding: utf-8 -*-

import typing as T
import uuid
import enum
from datetime import datetime, timezone
from functools import cached_property
from contextlib import contextmanager


import pynamodb
from pynamodb.models import (
    Model,
    PAY_PER_REQUEST_BILLING_MODE,
)
from pynamodb.indexes import (
    GlobalSecondaryIndex,
    KeysOnlyProjection,
)
from pynamodb.connection import Connection
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UTCDateTimeAttribute,
    MapAttribute,
    JSONAttribute,
)

connection = Connection()


EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class StatusEnum(int, enum.Enum):
    s00_todo = 0
    s03_in_progress = 3
    s06_failed = 6
    s09_success = 9
    s10_ignore = 10


class StatusAndTaskIdIndex(GlobalSecondaryIndex):
    """
    GSI for query by job_id and status
    """

    class Meta:
        index_name = "status_and_task_id-index"
        projection = KeysOnlyProjection()

    value: T.Union[str, UnicodeAttribute] = UnicodeAttribute(hash_key=True)
    key: T.Union[str, UnicodeAttribute] = UnicodeAttribute()


class LockError(Exception):
    pass


class IgnoreError(Exception):
    pass


_update_context: T.Dict[str, T.Dict[str, T.Any]] = dict()


class Tracker(Model):
    """

    :param key: The unique identifier of the task. It is a compound key of
        job_id and task_id. The format is ``{job_id}{separator}{task_id}``
    :param value: Indicate the status of the task. The format is
        ``{job_id}{separator}{status_code}``.
    :param update_time: when the task status is updated
    :param retry: how many times the task has been retried
    :param lock: a concurrency control mechanism. It is an uuid string.
    :param lock_time:
    :param data: arbitrary data in python dictionary.
    """

    class Meta:
        table_name = "tracker-pattern"
        region = "us-east-1"
        billing_mode = PAY_PER_REQUEST_BILLING_MODE

    # define attributes
    key: T.Union[str, UnicodeAttribute] = UnicodeAttribute(hash_key=True)
    value: T.Union[str, UnicodeAttribute] = UnicodeAttribute()
    update_time: T.Union[datetime, UTCDateTimeAttribute] = UTCDateTimeAttribute(
        default=utc_now,
    )
    retry: T.Union[int, NumberAttribute] = NumberAttribute(default=0)
    lock: T.Union[T.Optional[str], UnicodeAttribute] = UnicodeAttribute(
        default=None,
        null=True,
    )
    lock_time: T.Union[datetime, UTCDateTimeAttribute] = UTCDateTimeAttribute(
        default=EPOCH,
    )
    data: T.Optional[T.Union[dict, JSONAttribute]] = JSONAttribute(
        default=None, null=True
    )
    errors: T.Optional[T.Union[dict, JSONAttribute]] = JSONAttribute(
        default=None, null=True
    )

    status_and_task_id_index = StatusAndTaskIdIndex()

    SEP = "____"
    STATUS_ZERO_PAD = 2
    MAX_RETRY = 3
    LOCK_EXPIRE_SECONDS = 3600

    @classmethod
    def make_key(cls, job_id: str, task_id: str) -> str:
        return f"{job_id}{cls.SEP}{task_id}"

    @classmethod
    def make_value(cls, job_id: str, status: int) -> str:
        return f"{job_id}{cls.SEP}{str(status).zfill(cls.STATUS_ZERO_PAD)}"

    @cached_property
    def job_id(self) -> str:
        return self.key.split(self.SEP)[0]

    @cached_property
    def task_id(self) -> str:
        return self.key.split(self.SEP)[1]

    @cached_property
    def status(self) -> int:
        return int(self.value.split(self.SEP)[1])

    @classmethod
    def get_one(cls, job_id: str, task_id: str) -> "Tracker":
        return cls.get(cls.make_key(job_id, task_id))

    @classmethod
    def _make(
        cls,
        job_id: str,
        task_id: str,
        status: int,
    ) -> "Tracker":
        obj = cls(
            key=cls.make_key(job_id, task_id),
            value=cls.make_value(job_id, status),
        )
        obj.save()
        return obj

    @classmethod
    def new(cls, job_id: str, task_id: str) -> "Tracker":
        return cls._make(job_id, task_id, StatusEnum.s00_todo.value)

    @classmethod
    def delete_all(cls) -> int:
        ith = 0
        with cls.batch_write() as batch:
            for ith, item in enumerate(cls.scan(), start=1):
                batch.delete(item)
        return ith

    def is_locked(self) -> bool:
        if self.lock is None:
            return False
        else:
            now = utc_now()
            return (now - self.lock_time).total_seconds() < self.LOCK_EXPIRE_SECONDS

    @contextmanager
    def update_context(self) -> "Tracker":
        try:
            _update_context[self.key] = dict()
            yield self
        except Exception as e:
            raise e
        finally:
            actions = list(_update_context[self.key].values())
            # print(f"execute update: {actions}")
            if len(actions):
                self.update(actions=actions)
            del _update_context[self.key]

    def set_status(self, status: int) -> "Tracker":
        self.value = self.make_value(self.job_id, status)
        _update_context[self.key]["value"] = Tracker.value.set(self.value)
        return self

    def set_update_time(self, update_time: T.Optional[datetime] = None) -> "Tracker":
        if update_time is None:
            update_time = utc_now()
        self.update_time = update_time
        _update_context[self.key]["update_time"] = Tracker.update_time.set(
            self.update_time
        )
        return self

    def set_retry_as_zero(self) -> "Tracker":
        self.retry = 0
        _update_context[self.key]["retry"] = Tracker.retry.set(self.retry)
        return self

    def set_retry_plus_one(self) -> "Tracker":
        self.retry += 1
        _update_context[self.key]["retry"] = Tracker.retry.set(Tracker.retry + 1)
        return self

    def set_locked(self) -> "Tracker":
        self.lock = uuid.uuid4().hex
        self.lock_time = utc_now()
        _update_context[self.key]["lock"] = Tracker.lock.set(self.lock)
        _update_context[self.key]["lock_time"] = Tracker.lock_time.set(self.lock_time)
        return self

    def set_unlock(self) -> "Tracker":
        self.lock = None
        _update_context[self.key]["lock"] = Tracker.lock.set(self.lock)
        return self

    def set_data(self, data: T.Optional[dict]) -> "Tracker":
        self.data = data
        _update_context[self.key]["data"] = Tracker.data.set(data)
        return self

    def set_errors(self, errors: T.Optional[dict]) -> "Tracker":
        self.errors = errors
        _update_context[self.key]["data"] = Tracker.errors.set(errors)
        return self

    @contextmanager
    def start(
        self,
        in_process_status: int,
        failed_status: int,
        success_status: int,
        ignore_status: int,
    ) -> "Tracker":
        if self.is_locked():
            raise LockError(f"Task {self.key} is locked.")

        # if self.retry >= self.MAX_RETRY:
        #     raise Exception(f"Task {self.key} retry count exceeded {self.MAX_RETRY}, ignore it")

        # mark as in progress
        with self.update_context():
            (self.set_status(in_process_status).set_update_time().set_locked())

        with self.update_context():
            try:
                print("before yield")
                yield self
                print("after yield")
                self.set_status(
                    success_status
                ).set_update_time().set_unlock().set_retry_as_zero()
                print("end of success logic")
            except Exception as e:
                self.set_status(
                    failed_status
                ).set_update_time().set_unlock().set_errors(
                    {"error": str(e)}
                ).set_retry_plus_one()
                if self.retry == 3:
                    self.set_status(ignore_status)
                print("end of failed logic")
                raise e

    def start_job(
        self,
    ) -> "Tracker":
        return self.start(
            in_process_status=StatusEnum.s03_in_progress.value,
            failed_status=StatusEnum.s06_failed.value,
            success_status=StatusEnum.s09_success.value,
            ignore_status=StatusEnum.s10_ignore.value,
        )

    # @classmethod
    # def query_by_status(
    #     cls,
    #     status: T.Union[int, T.List[int]],
    #     limit: int = 10,
    # ) -> T.Iterable["TaskTracker"]:
    #     if isinstance(status, list):
    #         status_list = status
    #     else:
    #         status_list = [
    #             status,
    #         ]
    #     for status in status_list:
    #         yield from cls.job_id_and_status_index.query(
    #             hash_key=cls.make_value(status),
    #             limit=limit,
    #         )


# ------------------------------------------------------------------------------
# Unit test start here
# ------------------------------------------------------------------------------
import os
import pytest


class TestCase:
    @classmethod
    def setup_class(cls):
        Tracker.delete_all()

    def test(self):
        self.case_1_lock()

    def case_1_lock(self):
        job_id = "test"
        task_id = "t-1"

        tracker = Tracker.new(job_id, task_id=task_id)
        assert tracker.status == StatusEnum.s00_todo.value
        assert tracker.lock is None

        tracker = Tracker.get_one(job_id, task_id)
        assert tracker.status == StatusEnum.s00_todo.value
        assert tracker.lock is None

        assert tracker.is_locked() is False

        # lock it
        with tracker.update_context():
            tracker.set_locked()

        # set loc

        assert tracker.lock is not None
        assert tracker.is_locked() is True

        with tracker.start_job():
            tracker.set_data({"message": "hello"})


# if __name__ == "__main__":
#     import random
#
#     # Tracker.create_table(wait=True)
#


#
#     print("before start")
#     with tracker.start(
#         in_process_status=StatusEnum.s03_in_progress.value,
#         failed_status=StatusEnum.s06_failed.value,
#         success_status=StatusEnum.s09_success.value,
#         ignore_status=StatusEnum.s10_ignore.value,
#     ):
#         raise Exception("Something went wrong!")
#         data = {"a": random.randint(100, 199)}
#         print(data)
#         tracker.set_data(data)
#         # if random.randint(1, 10) <= 5:
#         #     raise Exception("Something went wrong!")
#         # else:
#         #     data = {"a": random.randint(100, 199)}
#         #     print(data)
#         #     tracker.set_data(data)
#     print("after start")


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
