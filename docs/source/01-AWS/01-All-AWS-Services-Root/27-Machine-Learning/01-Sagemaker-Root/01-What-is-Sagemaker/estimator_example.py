# -*- coding: utf-8 -*-

import sagemaker
from sagemaker import image_uris
from sagemaker.estimator import Estimator

sess = sagemaker.Session()
role = sagemaker.get_execution_role()
container = image_uris.retrieve("pca", "us-east-2", version="1")

pca = sagemaker.estimator.Estimator(
    container,
    role,
    instance_count=1,
    instance_type="ml.m4.xlarge",
    output_path="s3://my-bucket/prefix/pca/output".format(),
    sagemaker_session=sess,
)

pca_transformer = pca.transformer(
    instance_count=1,
    instance_type="ml.m4.xlarge",
    strategy="MultiRecord",
    assemble_with="Line",
    output_path="s3://my-bucket/prefix/pca/transform/train",
)

pca_transformer.transform(
    "s3://my-bucket/prefix/pca/transform/train/train.csv"
)



# image_uris.retrieve