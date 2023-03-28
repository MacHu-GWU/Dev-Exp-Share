Catalog Models with Model Registry
==============================================================================
ML 模型本质上就是一个容器. 所以逻辑上你可以用管理容器的方式来管理 ML. Amazon Sagemaker Model Registry 是 Amazon Sagemaker 的子服务, 本质上就是让数据科学家在不懂 Docker 的知识的情况下管理 ML 模型的版本.

Model Registry 有两个概念 Model Group 和 Model Package:

- Model Group: 就是一个模型的抽象, 你可以理解为 Docker 里的 Repository, 也可以理解为面向对象中的 类.
- Model Package: 则是一个模型的具体版本, 你可以理解为 Docker 里的 Tag, 也可以理解为面向对象中的 实例. 其中 Model Package 都有对应的版本号 Version, 版本号是从 1 开始的整数. 这一点跟 Lambda Function Version 类似.


Register Version
------------------------------------------------------------------------------
Reference:

- https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-version.html

.. code-block:: python

    # Specify the model source
    model_url = "s3://your-bucket-name/model.tar.gz"

    modelpackage_inference_specification =  {
        "InferenceSpecification": {
          "Containers": [
             {
                "Image": '257758044811.dkr.ecr.us-east-2.amazonaws.com/sagemaker-xgboost:1.2-1',
            "ModelDataUrl": model_url
             }
          ],
          "SupportedContentTypes": [ "text/csv" ],
          "SupportedResponseMIMETypes": [ "text/csv" ],
       }
     }

    # Alternatively, you can specify the model source like this:
    # modelpackage_inference_specification["InferenceSpecification"]["Containers"][0]["ModelDataUrl"]=model_url

    create_model_package_input_dict = {
        "ModelPackageGroupName" : model_package_group_name,
        "ModelPackageDescription" : "Model to detect 3 different types of irises (Setosa, Versicolour, and Virginica)",
        "ModelApprovalStatus" : "PendingManualApproval"
    }
    create_model_package_input_dict.update(modelpackage_inference_specification)

    create_model_package_response = sm_client.create_model_package(**create_model_package_input_dict)
    model_package_arn = create_model_package_response["ModelPackageArn"]
    print('ModelPackage Version ARN : {}'.format(model_package_arn))
Deploy Model
------------------------------------------------------------------------------
从一个已经注册号的 Model Package 部署一个模型有两种方式:

.. code-block:: python

    # 用 sagemaker SDK (高级封装 API)
    from sagemaker import ModelPackage
    from time import gmtime, strftime

    model_package_arn = 'arn:aws:sagemaker:us-east-1:12345678901:model-package/modeltest/1'
    model = ModelPackage(
        role=role,
        model_package_arn=model_package_arn,
        sagemaker_session=sagemaker_session,
    )
    model.deploy(initial_instance_count=1, instance_type='ml.m5.xlarge')

.. code-block:: python

    # 用 boto3 (底层 API)
    # 1. Create a model object from the model version
    model_name = (
        'DEMO-modelregistry-model-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime()
    )
    print("Model name : {}".format(model_name))
    container_list = [{'ModelPackageName': model_version_arn}]

    create_model_response = sm_client.create_model(
        ModelName = model_name,
        ExecutionRoleArn = role,
        Containers = container_list
    )
    print("Model arn : {}".format(create_model_response["ModelArn"]))

    # 2. Create an endpoint configuration
    endpoint_config_name = (
        'DEMO-modelregistry-EndpointConfig-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    )
    print(endpoint_config_name)
    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName = endpoint_config_name,
        ProductionVariants=[
            {
                'InstanceType':'ml.m4.xlarge',
                'InitialVariantWeight':1,
                'InitialInstanceCount':1,
                'ModelName':model_name,
                'VariantName':'AllTraffic'
            }
        ]
    )

    # 3. Create the endpoint
    endpoint_name = (
        'DEMO-modelregistry-endpoint-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime()
        )
    print("EndpointName={}".format(endpoint_name))

    create_endpoint_response = sm_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name,
    )
    print(create_endpoint_response['EndpointArn'])


Links
------------------------------------------------------------------------------
- Catalog Models with Model Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html
- Deploy a Model from Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html