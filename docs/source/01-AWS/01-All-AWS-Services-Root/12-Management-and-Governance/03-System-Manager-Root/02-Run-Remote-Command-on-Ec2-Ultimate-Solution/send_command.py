# -*- coding: utf-8 -*-

import typing as T
import sys
import enum
import time
import itertools
import dataclasses

if T.TYPE_CHECKING:
    from mypy_boto3_ssm.client import SSMClient


class Waiter:
    """
    Simple retry / polling with progressing status. Usage, it is common to check
    if a long-running job is done every X seconds and timeout in Y seconds.
    This class allow you to customize the polling interval and timeout,.

    Example:

    .. code-block:: python

        print("before waiter")

        for attempt, elapse in Waiter(
            delays=1,
            timeout=10,
            verbose=True,
        ):
            # check if should jump out of the polling loop
            if elapse >= 5:
                print("")
                break

        print("after waiter")
    """

    def __init__(
        self,
        delays: T.Union[int, float],
        timeout: T.Union[int, float],
        indent: int = 0,
        verbose: bool = True,
    ):
        self._delays = delays
        self.delays = itertools.repeat(delays)
        self.timeout = timeout
        self.tab = " " * indent
        self.verbose = verbose

    def __iter__(self):
        if self.verbose:  # pragma: no cover
            sys.stdout.write(
                f"start waiter, polling every {self._delays} seconds, "
                f"timeout in {self.timeout} seconds.\n"
            )
            sys.stdout.flush()
            sys.stdout.write(
                f"\r{self.tab}on 0 th attempt, "
                f"elapsed 0 seconds, "
                f"remain {self.timeout} seconds ..."
            )
            sys.stdout.flush()
        start = time.time()
        end = start + self.timeout
        yield 0, 0
        for attempt, delay in enumerate(self.delays, 1):
            now = time.time()
            remaining = end - now
            if remaining < 0:
                raise TimeoutError(f"timed out in {self.timeout} seconds!")
            else:
                time.sleep(min(delay, remaining))
                elapsed = int(now - start + delay)
                if self.verbose:  # pragma: no cover
                    sys.stdout.write(
                        f"\r{self.tab}on {attempt} th attempt, "
                        f"elapsed {elapsed} seconds, "
                        f"remain {self.timeout - elapsed} seconds ..."
                    )
                    sys.stdout.flush()
                yield attempt, int(elapsed)


def send_command(
    ssm_client,
    instance_id: str,
    commands: T.List[str],
) -> str:
    """
    Reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/send_command.html
    """
    res = ssm_client.send_command(
        InstanceIds=[
            instance_id,
        ],
        DocumentName="AWS-RunShellScript",
        DocumentVersion="1",
        Parameters={"commands": commands},
    )
    command_id = res["Command"]["CommandId"]
    return command_id


class CommandInvocationStatusEnum(str, enum.Enum):
    """
    Reference:

    - get_command_invocation_
    """

    Pending = "Pending"
    InProgress = "InProgress"
    Delayed = "Delayed"
    Success = "Success"
    Cancelled = "Cancelled"
    TimedOut = "TimedOut"
    Failed = "Failed"
    Cancelling = "Cancelling"


@dataclasses.dataclass
class CommandInvocation:
    """
    Represents a Command Invocation details returned from a
    get_command_invocation_ API call.
    """

    CommandId: T.Optional[str] = dataclasses.field(default=None)
    InstanceId: T.Optional[str] = dataclasses.field(default=None)
    Comment: T.Optional[str] = dataclasses.field(default=None)
    DocumentName: T.Optional[str] = dataclasses.field(default=None)
    DocumentVersion: T.Optional[str] = dataclasses.field(default=None)
    PluginName: T.Optional[str] = dataclasses.field(default=None)
    ResponseCode: T.Optional[int] = dataclasses.field(default=None)
    ExecutionStartDateTime: T.Optional[str] = dataclasses.field(default=None)
    ExecutionElapsedTime: T.Optional[str] = dataclasses.field(default=None)
    ExecutionEndDateTime: T.Optional[str] = dataclasses.field(default=None)
    Status: T.Optional[str] = dataclasses.field(default=None)
    StatusDetails: T.Optional[str] = dataclasses.field(default=None)
    StandardOutputContent: T.Optional[str] = dataclasses.field(default=None)
    StandardOutputUrl: T.Optional[str] = dataclasses.field(default=None)
    StandardErrorContent: T.Optional[str] = dataclasses.field(default=None)
    StandardErrorUrl: T.Optional[str] = dataclasses.field(default=None)
    CloudWatchOutputConfig: T.Optional[dict] = dataclasses.field(default=None)

    @classmethod
    def from_get_command_invocation_response(
        cls,
        response: dict,
    ) -> "CommandInvocation":
        """
        Reference:

        - get_command_invocation_
        """
        kwargs = {
            field.name: response.get(field.name) for field in dataclasses.fields(cls)
        }
        return cls(**kwargs)

    @classmethod
    def get(
        cls,
        ssm_client: "SSMClient",
        command_id: str,
        instance_id: str,
    ) -> "CommandInvocation":
        """
        A wrapper around get_command_invocation_ API call.

        Reference:

        - get_command_invocation_
        """
        response = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        return cls.from_get_command_invocation_response(response)

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


def wait_until_command_succeeded(
    ssm_client: "SSMClient",
    command_id: str,
    instance_id: str,
    delays: int = 3,
    timeout: int = 60,
    verbose: bool = True,
) -> CommandInvocation:
    """
    After you call send_command_ API, you can use this function to wait until
    it succeeds. If it fails, it will raise an exception.

    Reference:

    - get_command_invocation_
    """
    for _ in Waiter(delays=delays, timeout=timeout, verbose=verbose):
        command_invocation = CommandInvocation.get(
            ssm_client=ssm_client,
            command_id=command_id,
            instance_id=instance_id,
        )
        if command_invocation.Status == CommandInvocationStatusEnum.Success.value:
            sys.stdout.write("\n")
            return command_invocation
        elif command_invocation.Status in [
            CommandInvocationStatusEnum.Cancelled.value,
            CommandInvocationStatusEnum.TimedOut.value,
            CommandInvocationStatusEnum.Failed.value,
            CommandInvocationStatusEnum.Cancelling.value,
        ]:
            raise Exception(f"Command failed, status: {command_invocation.Status}")
        else:
            pass
