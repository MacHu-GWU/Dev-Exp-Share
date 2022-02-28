# -*- coding: utf-8 -*-

import uuid
import boto3
from rich import print
from pathlib_mate import Path
from s3pathlib import S3Path

boto_ses = boto3.session.Session()
tt_client = boto_ses.client("textract")
sm_client = boto_ses.client("sagemaker")

human_review_workflow_name = "a2i-textract-review-workflow"
task_template_name = "a2i-textract-review-workflow-task-template"

s3path = S3Path(
    "aws-data-lab-sanhe-for-everything",
    f"poc/2022-02-23-a2i/{human_review_workflow_name}/"
)
s3path_input = S3Path(s3path, "input/")
s3path_output = S3Path(s3path, "output/")
print(f"workflow output s3 uri: {s3path_output.uri}")



def run_textract_job():
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_document
    """
    p = Path("1.png")
    s3path = S3Path(s3path_input, "1.png")
    if not s3path.exists():
        s3path.upload_file(p.abspath, overwrite=True)

    human_loop_name = str(uuid.uuid4())
    print(f"human loop name: {human_loop_name}")
    res = tt_client.analyze_document(
        Document=dict(
            S3Object=dict(
                Bucket=s3path.bucket,
                Name=s3path.key,
            ),
        ),
        FeatureTypes=["FORMS",],
        HumanLoopConfig=dict(
            HumanLoopName=human_loop_name,
            FlowDefinitionArn=f"arn:aws:sagemaker:us-east-1:669508176277:flow-definition/{human_review_workflow_name}",
            DataAttributes=dict(
                ContentClassifiers=[
                    "FreeOfPersonallyIdentifiableInformation",
                    "FreeOfAdultContent",
                ]
            )
        ),
    )
    print(res)
#
# "s3://aws-data-lab-sanhe-for-everything/poc/2022-02-23-a2i/review-workflow/output"

# a2i_client = boto_ses.client('sagemaker-a2i-runtime')
# response = a2i_client.describe_human_loop(
#     HumanLoopName="test-human-loop"
# )
# print(response)


def inspect_human_review_workflow():
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_flow_definition
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.describe_flow_definition
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.delete_flow_definition
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.list_flow_definitions
    """
    res = sm_client.describe_flow_definition(
        FlowDefinitionName=human_review_workflow_name,
    )
    print(res)


if __name__ == "__main__":
    # inspect_human_review_workflow()
    run_textract_job()
    pass
