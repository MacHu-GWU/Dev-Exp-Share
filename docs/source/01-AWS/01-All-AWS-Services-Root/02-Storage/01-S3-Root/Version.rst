Version
==============================================================================


Managing Objects in a Versioning-Enabled Bucket
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/AmazonS3/latest/dev/manage-objects-versioned-bucket.html

- Add: 自动给予 Object 新的 VersionId.
- Get: 默认获得最新的, 要获得特定 Version, 需要指定 VersionId
- Delete: 如果不指定 VersionId, 则在最新的 Object 上加一个 Marker, 标记为已删除, 这个已删除的 Object 则会作为最新的 Object. 此时默认的 Get 操作则会返回 404 错误. 只有指定 VersionId, 才能真正删除某个 Version.


Managing Objects in a Versioning-Suspended Bucket
------------------------------------------------------------------------------

Reference: https://docs.aws.amazon.com/AmazonS3/latest/dev/VersionSuspendedBehavior.html

- Add: 新加的 Object 会使用 Null 作为 VersionId, 并不会覆盖以前有 VersionId 的 Object, 而新加的同 Key 的 Object 则会覆盖掉 Null VersionId 的 Object.
- Get: 无论你是否开启 Versioning, 永远是获取最新的那个 Object. Null 被视为最新的 Object.
- Delete: 只能删除 Null VersionId 的 Object, 无法删除之前的 Versioned Object.
