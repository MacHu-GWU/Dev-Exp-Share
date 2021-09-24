.. _aws-lake-formation-data-locations-permission:

Data Locations Permission
==============================================================================

在 Lake Formation 的 UI 中, 有一个 Register and Ingest -> Data Lake Locations 菜单, 和 Permission -> Data Locations 菜单. 从名字上看, 很难直观的看出这两个功能是做什么用的.

1. 首先要明白一点, 如果你给了用户 IAM Role S3 Read / Write 权限, 无论 Lake Formation 做什么, 你都无法阻止用户不通过任何 Athena Query 或是 Catalog, 直接访问 S3 中的数据. 所以我们在使用 Lake Formation 的时候, 不要直接给非 Admin 用户 S3 的权限.

2. 从菜单的名字上来看, 是不是你注册了 Data Lake Locations, 然后你在 Permission 中 Grant 给 IAM Role 这个 Location, 这个 IAM Role 就可以去 S3 访问数据了呢? 并不能. 因为该功能并不是 IAM 和 S3 Bucket Policy 的替代品. 请参考官方文档 https://docs.aws.amazon.com/lake-formation/latest/dg/access-control-underlying-data.html#data-location-permissions 中的这段话:

    Lake Formation data location permissions control the ability to create or alter Data Catalog resources that point to particular Amazon S3 locations. Data location permissions provide an extra layer of security to locations within the data lake. When you grant the CREATE_TABLE or ALTER permission to a principal, you also grant data location permissions to limit the locations for which the principal can create or alter metadata tables.

    意思是 ``data location permissions`` 控制的是指向该 s3 location 的 Data Catalog 中的 Create / Alter 的权限. 换言之, 如果没有这个功能, 用户只要有 Glue Catalog 或者 Crawler 的权限, 完全就可以自己创建一个 Glue Catalog Table, 然后用 Query 间接地把数据读出来. 这就属于 cascadence access 了. 当然, 你也不能允许一个没有 S3 权限但确有很大的 IAM 权限的 User 创建一个直接能 GetObject 的 EC2 从而把数据读出来. 这属于 IAM permission boundary 配置不当造成的, 不在本文讨论范围之内.
