# -*- coding: utf-8 -*-

import typing as T
import faker
import random
from rich import print as rprint
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_1")
context.attach_boto_session(bsm.boto_ses)

s3dir_root = S3Path.from_s3_uri(
    "s3://aws-data-lab-sanhe-for-everything/poc/2023-01-15-comprehend-training-data-format/"
).to_dir()
s3dir_train = s3dir_root.joinpath("train").to_dir()
s3dir_test = s3dir_root.joinpath("test").to_dir()
s3dir_output = s3dir_root.joinpath("output").to_dir()

n_record_per_file_train = 20
n_file_test = 10
n_record_test = 100
person_freq = 5
company_freq = 5

fake = faker.Faker()


def fake_person() -> T.Tuple[str, str]:
    label = "person"
    text = "{} {}. {}".format(
        fake.paragraph(10),
        ", ".join([fake.name() for _ in range(random.randint(3, 10))]),
        fake.paragraph(10),
    )
    return label, text


def fake_comapny() -> T.Tuple[str, str]:
    label = "company"
    text = "{} {}. {}".format(
        fake.paragraph(10),
        ", ".join(
            [
                f"{fake.company()} {fake.company_suffix()}"
                for _ in range(random.randint(3, 6))
            ]
        ),
        fake.paragraph(10),
    )
    return label, text


candidates = [fake_person,] * person_freq + [
    fake_comapny,
] * company_freq


def create_training():
    print(f"preview at: {s3dir_train.console_url}")
    s3dir_train.delete_if_exists()
    for nth_file in range(1, n_file_test + 1):
        lines = list()
        for _ in range(n_record_per_file_train):
            label, text = random.choice(candidates)()
            line = f'"{label}","{text}"'
            lines.append(line)
        s3path = s3dir_train.joinpath(f"train-{nth_file}.csv")
        s3path.write_text("\n".join(lines))


def create_classifier():
    """
    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.create_document_classifier
    """
    response = bsm.comprehend_client.create_document_classifier(
        DocumentClassifierName="PersonOrCompany",
        VersionName="v1",
        InputDataConfig=dict(
            DataFormat="COMPREHEND_CSV",
            S3Uri=s3dir_train.uri,
        ),
        DataAccessRoleArn="arn:aws:iam::669508176277:role/sanhe-comprehend-admin-access",
        LanguageCode="en",
        Mode="MULTI_CLASS",
    )
    rprint(response)


def create_test():
    print(f"preview at: {s3dir_test.console_url}")
    s3dir_test.delete_if_exists()

    lines = list()
    for _ in range(n_record_test):
        label, text = random.choice(candidates)()
        line = f'"{label}","{text}"'
        lines.append(line)
    s3path = s3dir_test.joinpath("test.csv")
    s3path.write_text("\n".join(lines))


def run_test():
    """
    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#Comprehend.Client.start_document_classification_job
    """
    start_response = ch_client.start_document_classification_job(
        InputDataConfig=dict(
            S3Uri=s3dir_text.uri,
            InputFormat="ONE_DOC_PER_FILE",
        ),
        OutputDataConfig=dict(
            S3Uri=s3dir_predict.uri,
        ),
        DataAccessRoleArn="arn:aws:iam::669508176277:role/sanhe-comprehend-admin-access",
        DocumentClassifierArn="arn:aws:comprehend:us-east-1:669508176277:document-classifier/MyClassifier8",
    )
    print(start_response)


# print(fake_person())
# print(fake_comapny())
# create_training()
create_classifier()
# create_test()
