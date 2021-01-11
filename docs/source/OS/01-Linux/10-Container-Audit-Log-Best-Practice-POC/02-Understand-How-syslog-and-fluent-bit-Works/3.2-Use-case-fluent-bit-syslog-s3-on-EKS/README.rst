Use case fluent-bit syslog s3 on EKS
==============================================================================

This AWS Blog `Centralized Container Logging with Fluent Bit <https://aws.amazon.com/blogs/opensource/centralized-container-logging-fluent-bit/>`_ gives us an example using fluent-bit to aggregate application log from k8s, and then process and analyze it in AWS Kinesis firehose. In ths example, it is simply INPUT=tail (log file on file system), OUTPUT=firehose.


Follow the AWS Blog, deploy the ``tail`` + ``firehose``
------------------------------------------------------------------------------

**First, ssh to the Amazon Linux EC2 like we did before**.


**Install and Set Up kubectl**::

    # Download the latest release with the command:
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

    # Make the kubectl binary executable.
    chmod +x ./kubectl

    # Move the binary in to your PATH.
    sudo mv ./kubectl /usr/local/bin/kubectl

    #Test to ensure the version you installed is up-to-date:
    kubectl version --client

Reference:

- Install and Set Up kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl/

**Configure Authentication to AWS EKS**::

    # verify your aws caller identity
    # The EKS cluster usually specified what IAM role it trust
    # This is defined at EKS cluster creation
    # The EC2 where kubectl is running on has to attached the IAM role
    # If not, EKS auth won't pass through even you gave your EC2 Admin IAM Role
    # In this case the IAM role is arn:aws:iam::496213958842:role/odp-eks-nbmAxSnm20201217151203708200000009
    aws sts get-caller-identity

    # Use the AWS CLI update-kubeconfig command to create or update your kubeconfig for your cluster.
    # this command actually create an ~/.kube/config file
    EKS_CLUSTER_NAME="odp-eks-nbmAxSnm"
    aws eks --region us-east-1 update-kubeconfig --name ${EKS_CLUSTER_NAME}

    # Verify ~/.kube/config file properly configured
    cat ~/.kube/config

    # Test your configuration.
    kubectl get svc
    kubectl

Reference:

- Create a kubeconfig for Amazon EKS: https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html

**Attach Policy File to EKS Work Node**::

Since fluent-bit will write output to firehose, the EKS node should be able to do that.

    ROLE_NAME="odp-eks-nbmAxSnm20201217151203708200000009"
    aws iam put-role-policy \
        --role-name ${ROLE_NAME} \
        --policy-name FluentBit-DaemonSet \
        --policy-document file://eks-fluent-bit-daemonset-policy.json


**Create a Service Account**::

    kubectl create sa fluent-bit


**Deploy Fluent-bit DaemonSet**::

    kubectl apply -f eks-fluent-bit-daemonset-rbac.yaml
    kubectl apply -f eks-fluent-bit-configmap.yaml
    kubectl apply -f eks-fluent-bit-daemonset.yaml
    kubectl apply -f eks-nginx-app.yaml


Tweak the script little bit, deploy the ``syslog`` + ``s3``
------------------------------------------------------------------------------

Note::

    Robert Lupinek - ISE-C1:47 PM
    eksctl get iamidentitymapping --cluster my-cluster-1
    Robert Lupinek - ISE-C1:48 PM
    kubectl edit configmap
