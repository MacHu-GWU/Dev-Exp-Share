# -*- coding: utf-8 -*-

# Standard Library
import uuid

# Third Party Library
import attr
from boto_session_manager import BotoSesManager, AwsServiceEnum
from pathlib_mate import Path

dir_here = Path.dir_here(__file__)


@attr.s
class Config:
    bsm: BotoSesManager = attr.ib()
    task_ui_name: str = attr.ib()
    task_ui_template: Path = attr.ib()

    flow_definition_name: str = attr.ib()
    hil_data_file: Path = attr.ib()

    sm_client = attr.ib(default=None)
    a2i_client = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.sm_client = self.bsm.get_client(AwsServiceEnum.SageMaker)
        self.a2i_client = self.bsm.get_client(AwsServiceEnum.AugmentedAIRuntime)
        self.iam_client = self.bsm.get_client(AwsServiceEnum.IAM)
        self.sts_client = self.bsm.get_client(AwsServiceEnum.STS)

    @property
    def task_ui_arn(self):
        return (
            f"arn:aws:sagemaker:{self.bsm.aws_region}:{self.bsm.aws_account_id}:"
            f"human-task-ui/{self.task_ui_name}"
        )

    @property
    def task_ui_console_url(self):
        return (
            f"https://console.aws.amazon.com/a2i/home?"
            f"region={self.bsm.aws_region}#/worker-task-templates/{self.task_ui_name}"
        )

    @property
    def flow_definition_arn(self):
        return (
            f"arn:aws:sagemaker:{self.bsm.aws_region}:{self.bsm.aws_account_id}:"
            f"flow-definition/{self.flow_definition_name}"
        )

    def create_human_task_ui(self, tags: dict = None) -> dict:
        print(f"Creating {self.task_ui_arn} ...")
        kwargs = dict(
            HumanTaskUiName=config.task_ui_name,
            UiTemplate=dict(
                Content=self.task_ui_template.read_text(encoding="utf-8"),
            ),
        )
        if tags:
            kwargs["Tags"] = [dict(Key=k, Value=v) for k, v in tags.items()]
        response = self.sm_client.create_human_task_ui(**kwargs)
        print(f"Success, preview at {self.task_ui_console_url}")
        return response

    def delete_human_task_ui(self) -> dict:
        print(f"Deleting {self.task_ui_arn} ...")
        response = self.sm_client.delete_human_task_ui(
            HumanTaskUiName=self.task_ui_name
        )
        print(f"Success, verify at {self.task_ui_console_url}")
        return response

    # --- Start Human in Loop
    @property
    def labeling_workforce_console_url(self) -> str:
        return (
            f"https://{self.bsm.aws_region}.console.aws.amazon.com/sagemaker/"
            f"groundtruth?region={self.bsm.aws_region}#/labeling-workforces"
        )

    def get_hil_console_url(self, hil_id: str) -> str:
        return (
            f"https://{self.bsm.aws_region}.console.aws.amazon.com/a2i/home?"
            f"region={self.bsm.aws_region}#/human-review-workflows/"
            f"{self.flow_definition_name}/human-loops/{hil_id}"
        )

    def start_human_loop(self):
        print("Start human loop ...")
        print(f"You can enter the labeling portal from {self.labeling_workforce_console_url}")
        response = self.a2i_client.start_human_loop(
            HumanLoopName=str(uuid.uuid4()),
            FlowDefinitionArn=self.flow_definition_arn,
            HumanLoopInput={
                "InputContent": self.hil_data_file.read_text(encoding="utf-8")
            }
        )
        hil_arn = response["HumanLoopArn"]
        hil_id = hil_arn.split("/")[-1]
        hil_console_url = self.get_hil_console_url(hil_id)
        print(f"Processing, preview HIL status at {hil_console_url}")



if __name__ == "__main__":
    config = Config(
        bsm=BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_1"),
        task_ui_name="a2i-poc-task-ui",
        task_ui_template=dir_here / "task.liquid",
        flow_definition_name="a2i-poc-flow-def",
        hil_data_file=dir_here / "task.json",
    )
    # config.delete_human_task_ui()
    # config.create_human_task_ui()
    config.start_human_loop()
