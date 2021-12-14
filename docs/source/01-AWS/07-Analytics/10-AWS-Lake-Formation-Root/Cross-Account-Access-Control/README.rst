Cross Account Access Control Using Lake Formation
==============================================================================



跨账号共享资源, 用 LF Tag 来管理访问权限
------------------------------------------------------------------------------

1. 所有的账号都要设置 Lake Formation Data Admin.
2. 你无法用 Lake Formation 把 Current Account 的 Resource 直接 Grant 给 External Account 中的某一个 Principal.
3. 你直接把 Resource Grant 给 External Account, Data Admin 需要接受, 接受后 External Account 的 Data Admin 就能在 Glue Catalog 里看到这些 Resource, 并且像管理 Current Account 中的 Catalog Database / Table 一样 Grant / Revoke 权限给当前账号 (External Account) 下的 Principal.

简单来说就是:

1. 每个 Account 的 Data Admin 管理自己 Account 下的 Resource
2. 想要共享资源, 例如 ResOnAccA 想要给 UserOnAccB, 那么 AccA 的 Admin 直接给对方 AccB, AccB 的 Admin 就自动获得 Resource 的权限, 然后 AccB 的 Admin 再把权限给 UserOnAccB.


To enable cross-account access, you grant Lake Formation permissions with the grant option on Data Catalog tables and databases (Data Catalog resources) to an external AWS account, organization, or organizational unit. The grant operation automatically shares those resources.

把 Res Grant 给一个 External Account / Organization / Org Unit, 那么这些 Resource 就可以被 External Account 下的所有 IAM User / Role 所访问.

You don't share resources with specific principals in external AWS accounts—you share the resources only with the accounts. Granting Lake Formation permissions to an organization or organizational unit is equivalent to granting the permission to every AWS account in that organization or organizational unit.

你不能把一个 Resource 直接给位于 External Account 下的某个具体的 Principal 例如 IAM Role. 你把 Permission 给了 Org 或者 Org Unit, 就相当于把权限给了下面所有的 AWS Account.

In each account that accesses a shared resource:

- At least one user must be a data lake administrator. For information on how to create a data lake administrator, see Create a Data Lake Administrator.
- The data lake administrator can view shared resources and grant Lake Formation permissions on the shared resources to other principals in the account. Other principals can't access shared resources until the data lake administrator grants them permissions on the resources. Because the data lake administrator must grant permissions on shared resources to the principals in the grantee account, cross-account permissions must always be granted with the grant option.
- For the data lake administrator and for principals whom the data lake administrator has granted permissions to, shared resources appear in the Data Catalog as if they were local (owned) resources. Extract, transform, and load (ETL) jobs can access the underlying data of shared resources.
- For shared resources, the Tables and Databases pages on the Lake Formation console display the owner's account ID.
- Principals can create a resource link in their Data Catalog to a shared resource from another AWS account. Integrated services such as Amazon Athena and Amazon Redshift Spectrum require resource links to be able to include shared resources in queries. For more information about resource links, see How Resource Links Work in Lake Formation.
- When the underlying data of a shared resource is accessed, AWS CloudTrail log events are generated in both the shared resource recipient's account and the resource owner's account. The CloudTrail events can contain the ARN of the principal that accessed the data, but only if the recipient account opts in to include the principal ARN in the logs. For more information, see Cross-Account CloudTrail Logging.



