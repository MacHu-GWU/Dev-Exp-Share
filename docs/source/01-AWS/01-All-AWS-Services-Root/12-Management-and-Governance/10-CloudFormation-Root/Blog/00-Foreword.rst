AWS Advance - Cloudformation Pro Foreword
==============================================================================

- Author: Sanhe Hu
- Announcement: Please Cite the Source of this post.

Recently I am deploying lots of AWS Resource, EC2, RDS, and Container. Then Infrastructure as Code (IAC) becomes the best solution for me.

In Cloud Computing Industry, every Cloud Vendor has its own implementation IAC. For example, Amazon Web Service has `Cloudformation <https://aws.amazon.com/cloudformation/>`_, Google Cloud Platform has `many Community Tools <https://cloud.google.com/solutions/infrastructure-as-code/#cards>`_, Microsoft Azure has `Azure Resource Manager <https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-overview>`_. Additional, the top open source IAC project `Terraform <https://www.terraform.io/>`_ implements the multi-Cloud Vendor compatible IAC.

**Then, how do I choose the IAC tools?**


How to Choose IAC Tools
------------------------------------------------------------------------------

First of all, the DevOps Engineer and the Tech Lead thinks in a very different way of choosing technique stacks.

As an engineer, they care about their own career path, **expecting to use minimal time, to learn minimal knowledge to solve most of the problems**. That's why Terraform becomes the most popular tool in the community. So you can use Terraform to work with different Cloud Vendor.

A tech lead usually prefers to choose the robust technology that can **minimize the probability to fail, minimize the time to pick up, require minimal knowledge**. In other words, **the technology should allow non-IAC-expert engineer to easily contribute robust code**. Of course, it has to meet the requirement on features, maintainability, and scalability.

**Enquizit** uses AWS as the primary Cloud Platform. And the native IAC Tool Cloudformation doesn't introduce much complex new Concept. Since JSON is so popular, every engineer can easily handle that. So internally, Enquizit chooses to use Cloudformation + Customized Plugin for IAC Practice.

I want to emphasize here, it is impossible to use a single tool or a single solution to solve all kinds of problems. Even though there are such tools like Terraform, which supports most of the cloud vendor, but in most of the time, it still takes deep dive into specific problems for a specific project. **In this IAC series of posts, I use CloudFormation as an example to discuss those common problems in IAC. Other platforms should have alternative solutions**.


Cloudformation Pro Series Topic
------------------------------------------------------------------------------

1. Manage Resource Dependencies.
2. Deploy Single Architect to Multiple Environment (dev/test/prod).
3. Cross Environment Dependencies.
4. Parameterize the Architect Design.
5. Batch Declaration multiple Resource in the same Type.
6. Orchestration.
7. Automate Deployment, CI/CD.
8. Reusability.
9. Others.

Here We Go!
