import boto3

sagemaker_client = boto3.client("sagemaker")

kwargs = {
    "ModelPackageGroupName": "my_model_pacakge_group_name",
    "ModelPackageDescription": "Model to detect 3 different types of irises (Setosa, Versicolour, and Virginica)",
    "ModelApprovalStatus": "PendingManualApproval",
    "InferenceSpecification": {
        "Containers": [
            {
                "Image": "257758044811.dkr.ecr.us-east-2.amazonaws.com/sagemaker-xgboost:1.2-1",
                "ModelDataUrl": "s3://your-bucket-name/model.tar.gz"
            }
        ],
        "SupportedContentTypes": ["text/csv"],
        "SupportedResponseMIMETypes": ["text/csv"],
    }
}

create_model_package_response = sagemaker_client.create_model_package(**kwargs)
model_package_arn = create_model_package_response["ModelPackageArn"]
print(f"ModelPackage Version ARN : {model_package_arn}")
