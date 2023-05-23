#----------------------------------------------------------------------#
# Lambda for Stack Creation
#----------------------------------------------------------------------#
import boto3
def lambda_handler(event, context):
    Region = event['region']
    Account = event['account']
    RepositoryName = event['detail']['repositoryName']
    NewBranch = event['detail']['referenceName']
    Event = event['detail']['event']
    if NewBranch == "master":
        quit()
    if Event == "referenceCreated":
        cf_client = boto3.client('cloudformation')
        cf_client.create_stack(
            StackName=f'Pipeline-{RepositoryName}-{NewBranch}',
            TemplateURL=f'https://s3.amazonaws.com/{Account}-templates/TemplatePipeline.yaml',
            Parameters=[
                {
                    'ParameterKey': 'RepositoryName',
                    'ParameterValue': RepositoryName,
                    'UsePreviousValue': False
                },
                {
                    'ParameterKey': 'BranchName',
                    'ParameterValue': NewBranch,
                    'UsePreviousValue': False
                }
            ],
            OnFailure='ROLLBACK',
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
    else:
        cf_client = boto3.client('cloudformation')
        cf_client.delete_stack(
            StackName=f'Pipeline-{RepositoryName}-{NewBranch}'
        )