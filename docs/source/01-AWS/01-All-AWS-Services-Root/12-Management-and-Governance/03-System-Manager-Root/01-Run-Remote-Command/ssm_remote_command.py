# -*- coding: utf-8 -*-

"""
This module allow you to run remote command on EC2 instance via SSM in 'sync' mode.
The original ssm_client.send_command() is 'async' call, which means you have to
poll the status of the command execution via ssm_client.get_command_invocation().
This module hides the complexity of polling and provide a simple interface.

Example:

.. code-block:: python

    import boto3
    from s3pathlib import S3Path

    instance_id = "i-1a2b3c"
    commands = [
        "echo hello"
    ]
    ssm_client = boto3.client("ssm")

    # make sure your EC2 has the IAM permission to write to this location
    s3dir_command_output = S3Path(f"s3://my-bucket/ssm-command-output/").to_dir()

    res = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        DocumentVersion="1",
        Parameters={
            "commands": commands
        },
        OutputS3BucketName=s3dir_command_output.bucket,
        OutputS3KeyPrefix=s3dir_command_output.key,
    )
    command_id = res["Command"]["CommandId"]

    wait_until_command_succeeded(
        ssm_client=ssm_client,
        command_id=command_id,
        instance_id=instance_id,
        delays=3,
        timeout=60,
        verbose=True,
    )

    for s3path in (
        s3dir_command_output.joinpath(
            command_id,
            instance_id,
            "awsrunShellScript",
        )
        .to_dir()
        .iter_objects()
    ):
        print(f"--- {s3path.uri} ---")
        print(f"{s3path.read_text()}")


.. _send_command: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/send_command.html
.. _get_command_invocation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_command_invocation.html
"""

import typing as T
import sys
import enum
import time
import itertools
import dataclasses

from func_args import resolve_kwargs, NOTHING

if T.TYPE_CHECKING:
    from mypy_boto3_ssm.client import SSMClient


class Waiter:
    """
    Simple retry / poll with progress.
    """

    def __init__(
        self,
        delays: T.Union[int, float],
        timeout: T.Union[int, float],
        indent: int = 0,
        verbose: bool = True,
    ):
        self.delays = itertools.repeat(delays)
        self.timeout = timeout
        self.tab = " " * indent
        self.verbose = verbose

    def __iter__(self):
        start = time.time()
        end = start + self.timeout
        for attempt, delay in enumerate(self.delays, 1):
            now = time.time()
            remaining = end - now
            if remaining < 0:
                raise TimeoutError(f"timed out in {self.timeout} seconds!")
            else:
                time.sleep(min(delay, remaining))
                elapsed = int(now - start + delay)
                if self.verbose:
                    sys.stdout.write(
                        f"\r{self.tab}on {attempt} th attempt, "
                        f"elapsed {elapsed} seconds, "
                        f"remain {self.timeout - elapsed} seconds ..."
                    )
                    sys.stdout.flush()
                yield attempt, int(elapsed)


class CommandInvocationStatusEnum(str, enum.Enum):
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
    Reference:

    - get_command_invocation_
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
        cls, response: dict
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
        plugin_name: T.Optional[str] = NOTHING,
    ) -> "CommandInvocation":
        """
        Reference:

        - get_command_invocation_
        """
        response = ssm_client.get_command_invocation(
            **resolve_kwargs(
                CommandId=command_id,
                InstanceId=instance_id,
                PluginName=plugin_name,
            )
        )
        return cls.from_get_command_invocation_response(response)


def wait_until_command_succeeded(
    ssm_client: "SSMClient",
    command_id: str,
    instance_id: str,
    plugin_name: T.Optional[str] = NOTHING,
    delays: int = 3,
    timeout: int = 60,
    verbose: bool = True,
):
    """
    Reference:

    - get_command_invocation_
    """
    for _ in Waiter(delays=delays, timeout=timeout, verbose=verbose):
        command_invocation = CommandInvocation.get(
            ssm_client=ssm_client,
            command_id=command_id,
            instance_id=instance_id,
            plugin_name=plugin_name,
        )
        if command_invocation.Status == CommandInvocationStatusEnum.Success.value:
            if verbose:
                print("")
            break
        elif command_invocation.Status in [
            CommandInvocationStatusEnum.Cancelled.value,
            CommandInvocationStatusEnum.TimedOut.value,
            CommandInvocationStatusEnum.Failed.value,
            CommandInvocationStatusEnum.Cancelling.value,
        ]:
            raise Exception(f"Command failed, status: {command_invocation.Status}")
        else:
            pass


if __name__ == "__main__":
    import boto3
    from s3pathlib import S3Path

    instance_id = "i-1a2b3c"
    commands = ["echo hello"]
    ssm_client = boto3.client("ssm")

    # make sure your EC2 has the IAM permission to write to this location
    s3dir_command_output = S3Path(f"s3://my-bucket/ssm-command-output/").to_dir()

    res = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        DocumentVersion="1",
        Parameters={"commands": commands},
        OutputS3BucketName=s3dir_command_output.bucket,
        OutputS3KeyPrefix=s3dir_command_output.key,
    )
    command_id = res["Command"]["CommandId"]

    wait_until_command_succeeded(
        ssm_client=ssm_client,
        command_id=command_id,
        instance_id=instance_id,
        delays=3,
        timeout=60,
        verbose=True,
    )

    for s3path in (
        s3dir_command_output.joinpath(
            command_id,
            instance_id,
            "awsrunShellScript",
        )
        .to_dir()
        .iter_objects()
    ):
        print(f"--- {s3path.uri} ---")
        print(f"{s3path.read_text()}")
