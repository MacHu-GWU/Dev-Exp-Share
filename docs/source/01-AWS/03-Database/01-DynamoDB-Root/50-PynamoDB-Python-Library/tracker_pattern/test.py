# -*- coding: utf-8 -*-


import pytest
import enum
import time
from tracker import (
    LockError,
    IgnoreError,
    EPOCH,
    utc_now,
    Tracker as BaseTracker,
)


class StatusEnum(int, enum.Enum):
    s00_todo = 0
    s03_in_progress = 3
    s06_failed = 6
    s09_success = 9
    s10_ignore = 10


class Tracker(BaseTracker):
    DEFAULT_STATUS = StatusEnum.s00_todo.value

    def start_job(
        self,
    ) -> "Tracker":
        """
        This is just an example of how to use :meth:`Tracker.start`.

        A job should always have four related status codes:

        - in process status
        - failed status
        - success status
        - ignore status

        If you have multiple type of jobs, I recommend creating multiple
        wrapper functions like this for each type of jobs. And ensure that
        the "ignore" status value is the largest status value among all,
        and use the same "ignore" status value for all type of jobs.
        """
        return self.start(
            in_process_status=StatusEnum.s03_in_progress.value,
            failed_status=StatusEnum.s06_failed.value,
            success_status=StatusEnum.s09_success.value,
            ignore_status=StatusEnum.s10_ignore.value,
        )


class UserError(Exception):
    pass


job_id = "test"


class TestTracker:
    @classmethod
    def setup_class(cls):
        Tracker.create_table(wait=True)
        Tracker.delete_all()

    def test(self):
        self._test_update_context()

        self._test_1_happy_path()
        self._test_2_lock_mechanism()
        self._test_3_retry_and_ignore()

        self._test_11_query_by_status()

    def _test_update_context(self):
        task_id = "t-0"

        tracker = Tracker.new(job_id, task_id)
        assert tracker.job_id == job_id
        assert tracker.task_id == task_id
        assert tracker.status == StatusEnum.s00_todo.value
        assert tracker.retry == 0
        assert (utc_now() - tracker.update_time).total_seconds() < 1
        assert tracker.lock is None
        assert tracker.lock_time == EPOCH
        assert tracker.data is None
        assert tracker.errors is None

        with tracker.update_context():
            tracker.set_status(status=StatusEnum.s03_in_progress.value)
            tracker.set_retry_plus_one()
            tracker.set_data({"version": 1})
            tracker.set_errors({"error": "something is wrong"})

        assert tracker.status == StatusEnum.s03_in_progress.value
        assert tracker.retry == 1
        assert tracker.data == {"version": 1}
        assert tracker.errors == {"error": "something is wrong"}

        tracker.refresh()
        assert tracker.status == StatusEnum.s03_in_progress.value
        assert tracker.retry == 1
        assert tracker.data == {"version": 1}
        assert tracker.errors == {"error": "something is wrong"}

        with pytest.raises(UserError):
            with tracker.update_context():
                tracker.set_data({"version": 2})
                raise UserError

        # when update fail, the attribute value will not be updated
        assert tracker.data == {"version": 1}

    def _test_1_happy_path(self):
        task_id = "t-1"

        # create a new tracker
        tracker = Tracker.new(job_id, task_id, data={"version": 1})
        assert tracker.status == StatusEnum.s00_todo.value

        # start the job, this time it will succeed
        with tracker.start_job():
            # check if the job status became "in progress"
            assert tracker.status == StatusEnum.s03_in_progress.value
            tracker.refresh()
            assert tracker.status == StatusEnum.s03_in_progress.value

            # do some work
            tracker.set_data({"version": 2})

        # check if the job status become "success"
        assert tracker.status == StatusEnum.s09_success.value
        assert tracker.data == {"version": 2}
        assert tracker.retry == 0
        tracker.refresh()
        assert tracker.status == StatusEnum.s09_success.value
        assert tracker.data == {"version": 2}
        assert tracker.retry == 0

        # start another job, this time it will fail
        tracker = Tracker.new(job_id, task_id, data={"version": 1})
        try:
            with tracker.start_job():
                tracker.set_data({"version": 2})
                raise UserError("something is wrong!")
        except UserError:
            pass

        assert tracker.status == StatusEnum.s06_failed.value
        assert tracker.data == {"version": 1}  # it is clean data
        assert tracker.retry == 1
        tracker.refresh()
        assert tracker.status == StatusEnum.s06_failed.value
        assert tracker.data == {"version": 1}  # it is the database side data
        assert tracker.retry == 1

    def _test_2_lock_mechanism(self):
        task_id = "t-2"

        # create a new tracker
        tracker = Tracker.new(job_id, task_id)
        assert tracker.status == StatusEnum.s00_todo.value
        assert tracker.lock is None
        assert tracker.is_locked() is False

        tracker = Tracker.get_one(job_id, task_id)
        assert tracker.status == StatusEnum.s00_todo.value
        assert tracker.lock is None
        assert tracker.is_locked() is False

        # lock it
        with tracker.update_context():
            tracker.set_locked()

        # verify it is really locked
        assert tracker.lock is not None
        assert tracker.is_locked() is True

        # run a job while it is locked
        assert tracker.data is None

        with pytest.raises(LockError):
            with tracker.start_job():
                tracker.set_data({"version": 2})

        # nothing should happen
        # data is not changed
        assert tracker.is_locked() is True
        assert tracker.data is None

        # status and update_time is not changed
        update_time = tracker.update_time
        tracker.refresh()
        assert tracker.update_time == update_time

    def _test_3_retry_and_ignore(self):
        task_id = "t-3"

        # create a new tracker
        tracker = Tracker.new(job_id, task_id, data={"version": 1})
        assert tracker.retry == 0

        # 1st try
        with pytest.raises(UserError):
            with tracker.start_job():
                raise UserError

        assert tracker.retry == 1
        assert tracker.status == StatusEnum.s06_failed.value
        tracker.refresh()
        assert tracker.retry == 1
        assert tracker.status == StatusEnum.s06_failed.value

        # 2nd try
        with pytest.raises(UserError):
            with tracker.start_job():
                raise UserError

        assert tracker.retry == 2
        assert tracker.status == StatusEnum.s06_failed.value
        tracker.refresh()
        assert tracker.retry == 2
        assert tracker.status == StatusEnum.s06_failed.value

        # 3rd try success, the retry reset to 0
        with tracker.start_job():
            tracker.set_data({"version": 2})
        assert tracker.retry == 0
        assert tracker.status == StatusEnum.s09_success.value
        assert tracker.data == {"version": 2}
        tracker.refresh()
        assert tracker.retry == 0
        assert tracker.status == StatusEnum.s09_success.value
        assert tracker.data == {"version": 2}

        # make three attempts to fail
        for _ in range(Tracker.MAX_RETRY):
            with pytest.raises(UserError):
                with tracker.start_job():
                    raise UserError

        assert tracker.retry == Tracker.MAX_RETRY
        assert tracker.status == StatusEnum.s10_ignore.value
        tracker.refresh()
        assert tracker.retry == Tracker.MAX_RETRY
        assert tracker.status == StatusEnum.s10_ignore.value

        with pytest.raises(IgnoreError):
            with tracker.start_job():
                tracker.set_data({"version": 3})

        assert tracker.retry == Tracker.MAX_RETRY
        assert tracker.status == StatusEnum.s10_ignore.value
        assert tracker.data == {"version": 2}
        tracker.refresh()
        assert tracker.retry == Tracker.MAX_RETRY
        assert tracker.status == StatusEnum.s10_ignore.value
        assert tracker.data == {"version": 2}

    def _test_11_query_by_status(self):
        job_id = "query_by_status"

        with Tracker.batch_write() as batch:
            batch.save(Tracker.make(job_id, "t-1", status=StatusEnum.s00_todo.value))
            batch.save(
                Tracker.make(job_id, "t-2", status=StatusEnum.s03_in_progress.value)
            )
            batch.save(Tracker.make(job_id, "t-3", status=StatusEnum.s06_failed.value))
            batch.save(Tracker.make(job_id, "t-4", status=StatusEnum.s09_success.value))
            batch.save(Tracker.make(job_id, "t-5", status=StatusEnum.s10_ignore.value))

        time.sleep(3)

        for ith, status in enumerate(StatusEnum, start=1):
            res = list(Tracker.query_by_status(job_id, status.value))
            assert len(res) == 1
            assert res[0].task_id == f"t-{ith}"

        res = list(
            Tracker.query_by_status(
                job_id,
                [
                    StatusEnum.s00_todo.value,
                    StatusEnum.s06_failed.value,
                ],
            )
        )
        assert len(res) == 2
        assert res[0].task_id == f"t-1"
        assert res[1].task_id == f"t-3"


if __name__ == "__main__":
    import sys
    import subprocess
    from pathlib import Path

    dir_here = Path(__file__).absolute().parent
    dir_htmlcov = dir_here / "htmlcov"
    path_cov_index_html = dir_htmlcov / "index.html"

    # virtual environment
    dir_bin = Path(sys.executable).parent
    bin_pytest = dir_bin / "pytest"

    def _run_cov_test(
        bin_pytest: str,
        script: str,
        module: str,
        root_dir: str,
        htmlcov_dir: str,
    ):
        """
        A simple wrapper around pytest + coverage cli command.
        :param bin_pytest: the path to pytest executable
        :param script: the path to test script
        :param module: the dot notation to the python module you want to calculate
            coverage
        :param root_dir: the dir to dump coverage results binary file
        :param htmlcov_dir: the dir to dump HTML output
        """
        args = [
            bin_pytest,
            "-s",
            "--tb=native",
            f"--rootdir={root_dir}",
            f"--cov={module}",
            "--cov-report",
            "term-missing",
            "--cov-report",
            f"html:{htmlcov_dir}",
            script,
        ]
        print(" ".join(args))
        subprocess.run(args)

    def run_cov_test(script: str, module: str, preview: bool = False):
        _run_cov_test(
            bin_pytest=f"{bin_pytest}",
            script=script,
            module=module,
            root_dir=f"{dir_here}",
            htmlcov_dir=f"{dir_htmlcov}",
        )
        if preview:
            subprocess.run(["open", f"{path_cov_index_html}"])

    run_cov_test(__file__, "tracker", preview=False)
