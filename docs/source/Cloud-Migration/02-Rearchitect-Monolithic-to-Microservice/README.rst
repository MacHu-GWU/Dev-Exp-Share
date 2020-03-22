Re-architect / Migrate Monolithic to Microservice
==============================================================================

将一个大型应用迁徙到 Microservice 的模式是非常复杂的.

1. 将大型应用的众多功能分拆成粒度大小合适的服务, 从设计上来说, 很难一次到位设计正确. 如果想充分考虑, 设计一个完美方案, 这个过程非常长.
2. 在服务不中断的情况下做系统迁徙, 由于新系统开发时间长, 即使你使用 Blue Green 的模式进行切换, 但你很难保证新系统的功能和原系统的功能保持一致.
3. 工程师团队转换思维的学习成本高, 很难一次做对.

那么如何让 Microservice 模式落地呢?


1. Technique Overhead
------------------------------------------------------------------------------

Setup these:

- Service Discovery
- API Gateway
- Service Mesh
- Service Development, Deployment (Blue Green, Canary) workflow


2. Migration
------------------------------------------------------------------------------

1. Start with taking one business logic out and migrate to a service. Such as Authentication, Data Pull.
2. Development, and Deploy.
3. Update Client Side Code, migrate.
4. Testing.
5. Come up platform / language specified workflow.

Repeat #1 ~ #5 for other business logic.
