MLOps foundation roadmap for enterprises with Amazon SageMaker
==============================================================================

好文解读:

- MLOps 在企业中从稚嫩到成熟: https://aws.amazon.com/blogs/machine-learning/mlops-foundation-roadmap-for-enterprises-with-amazon-sagemaker/


MLOps maturity model
------------------------------------------------------------------------------

- Initial: establish the experimental environment
- Repeatable: standardize code repository & ML solution deployment
- Reliable: introducing testing, monitoring, and multi-account deployment
- Scalable: Templatize and productionize multiple ML solution

**Initial phase**: During this phase, the data scientists are able to experiment and build, train, and deploy models on AWS using SageMaker services. The suggested development environment is Amazon SageMaker Studio, in which the data scientists are able to experiment and collaborate based on Studio notebooks.

**Repeatable phase** – With the ability to experiment on AWS, the next step is to create automatic workflows to preprocess data and build and train models (ML pipelines). Data scientists collaborate with ML engineers in a separate environment to build robust and production-ready algorithms and source code, orchestrated using Amazon SageMaker Pipelines. The generated models are stored and benchmarked in the Amazon SageMaker model registry.

**Reliable phase** – Even though the models have been generated via the ML pipelines, they need to be tested before they get promoted to production. Therefore, in this phase, the automatic testing methodology is introduced, for both the model and triggering infrastructure, in an isolated staging (pre-production) environment that simulates production. After a successful run of the test, the models are deployed to the isolated environment of production. To promote the models among the multiple environments, manual evaluation and approvals are required.

**Scalable phase** – After the productionization of the first ML solution, scaling of the MLOps foundation to support multiple data science teams to collaborate and productionize tens or hundreds of ML use cases is necessary. In this phase, we introduce the templatization of the solutions, which brings speed to value by reducing the development time of new production solutions from weeks to days. Additionally, we automate the instantiation of secure MLOps environments to enable multiple teams to operate on their data reducing the dependency and overhead to IT.

- **Flexibility** – Data scientists are able to accommodate any framework (such as TensorFlow or PyTorch)
- **Reproducibility** – Data scientists are able to recreate or observe past experiments (code, data, and results)
- **Reusability** – Data scientists and ML engineers are able to reuse source code and ML pipelines, avoiding inconsistencies and cost
- **Scalability** – Data scientists and ML engineers are able to scale resources and services on demand
- **Auditability** – Data scientists, IT, and legal departments are able to audit logs, versions, and dependencies of artifacts and data
- **Consistency** – Because MLOps consists of multiple environments, the foundation needs to eliminate variance between environments


Initial phase
------------------------------------------------------------------------------


Repeatable phase
------------------------------------------------------------------------------


From notebooks to ML pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Standardising repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Standardising repository branching and CI/CD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Standardising data structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Reliable phase
------------------------------------------------------------------------------

Data lake and MLOps integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Scalable Phase
------------------------------------------------------------------------------

