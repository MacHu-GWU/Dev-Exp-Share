# -*- coding: utf-8 -*-

import typing as T
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class StatusEnum:
    todo = 0
    failed = 20
    processing = 30
    finished = 50
    ignore = 70


class Task:
    def get_status(self) -> int:
        """
        获得当前 Task 的状态.
        """
        raise NotImplementedError

    def set_status(self, status: int):
        """
        设置 Task 的状态, 并将状态改变入库.
        """
        raise NotImplementedError

    def lock(self):
        """
        锁定 Task, 避免其他 Worker 处理同一个任务.
        """
        raise NotImplementedError

    def unlock(self):
        """
        解锁 Task.
        """
        raise NotImplementedError

    def is_locked(self) -> bool:
        """
        检查 Task 是否被锁死.
        """
        raise NotImplementedError


class Worker:
    def process_low_level_api(self, task: 'Task'):
        """
        实际执行业务的逻辑, 期间不要对 Task 的状态进行修改, 也不要对 Task 的更改进行入库.
        """
        raise NotImplementedError

    def process(self, task: 'Task'):
        """
        对底层的业务逻辑函数的封装, 根据异常的情况对 Task 的状态进行修改并入库.
        """
        raise NotImplementedError


class Coordinator:
    def init_task(self, task: 'Task'):
        """
        在后端数据库中初始化一个任务.
        """
        raise NotImplementedError

    def init_many_task(self, task_list: T.List['Task']):
        """
        在后端数据库中初始化很多个任务. 有的数据库 Batch 会有性能优势.
        """
        raise NotImplementedError

    def get_unfinished_task(self, limit: int) -> T.List['Task']:
        """
        从数据库中获得未完成的 Task
        """
        raise NotImplementedError

    def invoke_worker(self, task: 'Task'):
        """
        将 Task 交给 Worker 执行. 通常是远程异步调用.
        """
        raise NotImplementedError

    def loop(self):
        """
        执行一个循环, 通常包含:

        1. 初始化新 Task
        2. 获得未完成 Task
        3. 将其交给 Worker 执行

        一个循环的间隔时间建议是和 Task 执行的平均时间相近, 这样能最大化的利用资源.
        """
        for task in self.get_unfinished_task(limit=10):
            self.invoke_worker(task)


if __name__ == "__main__":
    # 下面我们实现了一个纯内存的 Use Case, Coordinator 和 Worker 都在本机运行
    # Worker 有 50% 的概率失败
    # 我们用 dictionary 来模拟数据库
    import random
    import dataclasses

    tracker: T.Dict[str, 'MyTask'] = dict()

    MAX_RETRY = 3
    LOCK_EXPIRE_SECONDS = 3600


    @dataclasses.dataclass
    class MyTask(Task):
        key: str
        status: int = StatusEnum.todo
        retry: int = 0
        locked: bool = False
        last_lock_time: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc)
        data: T.Optional[dict] = None

        def get_status(self) -> int:
            return self.status

        def set_status(self, status: int):
            self.status = status

        def lock(self):
            self.locked = True
            self.last_lock_time = utc_now()

        def unlock(self):
            self.locked = False

        def is_locked(self) -> bool:
            if self.locked is False:
                return False
            else:
                now = utc_now()
                return ((now - self.last_lock_time).total_seconds() < LOCK_EXPIRE_SECONDS)


    @dataclasses.dataclass
    class MyWorker(Coordinator):
        def process_low_level_api(self, task: 'MyTask'):
            print(f"Working on {task.key}")
            if random.randint(1, 100) <= 50:  # 以 50% 的概率失败
                raise ValueError("Something wrong!")
            print("  SUCCESS!")

        def process(self, task: 'MyTask'):
            # 执行任务之前先锁定 task
            task.lock()
            try:
                # 执行业务逻辑
                self.process_low_level_api(task)
                # 如果成功则更新状态, 解锁, 并入库
                task.status = StatusEnum.finished
                task.unlock()
            except Exception as e:
                print(f"  got error: {e}")
                # 如果失败, 则重试次数加 1
                task.retry += 1
                # 重试次数到达阈值, 则标记为 ignore, 不再重试
                if task.retry == MAX_RETRY:
                    task.status = StatusEnum.ignore
                # 没有到达阈值, 标记为 failed
                else:
                    task.status = StatusEnum.failed
                # 解锁, 并入库
                task.unlock()
            print(f"  after process, task = {task}")


    @dataclasses.dataclass
    class MyCoordinator(Coordinator):
        def init_task(self, task: 'MyTask'):
            tracker.setdefault(task.key, task)

        def init_many_task(self, task_list: T.List['MyTask']):
            for task in task_list:
                self.init_task(task)

        def get_unfinished_task(self, limit: int = 2) -> T.List['MyTask']:
            task_list = list()
            counter = 0
            for task_key, task in tracker.items():
                if task.status < StatusEnum.finished:
                    task_list.append(task)
                    counter += 1
                    if counter == limit:
                        break
            return task_list

        def invoke_worker(self, task: 'MyTask'):
            if task.is_locked() is False:
                my_worker.process(task)

        def loop(self):
            for task in self.get_unfinished_task():
                self.invoke_worker(task)


    my_coord = MyCoordinator()
    my_worker = MyWorker()

    # 一开始我们有 10 个任务
    # 每次我们派 2 个 worker 执行, 由于有 50% 的失败概率
    # 所以大约需要 10 次 loop 才能全部执行完成
    task_list = [
        MyTask(key=str(id).zfill(3))
        for id in range(1, 10 + 1)
    ]
    my_coord.init_many_task(task_list)

    n_loop = 10
    for i in range(1, 1 + n_loop):
        print(f"====== Loop {i} ======")
        my_coord.loop()
