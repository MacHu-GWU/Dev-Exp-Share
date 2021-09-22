

I am new to Lake Formation, I am trying to play with the LF-Tag based access control. I personally have some LakeForamtion question.

I have a dataset in S3, here's the S3 Folder Structure::

    s3://${bucket}/.../glue_resource_policy_poc/ # a dummy e-commerce dataset
    s3://${bucket}/.../glue_resource_policy_poc/users/
        user_id email       ssn
        uid-1   a@z.com     111-111-1111
        uid-2   b@z.com     222-222-2222
    s3://${bucket}/.../glue_resource_policy_poc/items/
        ...
    s3://${bucket}/.../glue_resource_policy_poc/orders/
        ...

I created an Assumed IAM Role and wanna test the access with the IAM Role. What I want to archive is:

1. the Admin IAM User (my main) can access anything, can run query via Athena to all table
2. the Assumed IAM Role can only query ``items`` and ``users.user_id, users.email`` but not ``users.ssn`` column, and get denied to query ``orders`` table

My Questions are:

1. Do I have to register it to LakeFormation Data Location? Can I run crawler and create table in Glue and then start playing LakeFormation, in other word, how can I use LakeFormation to manage existing access to Glue Database and Table?
2. I find out that once I add myself to LakeFormation admin. New glue crawler using my old Glue IAM Role stop working, cannot access to the new Table anymore. I think LakeFormation did some restriction under the hood, but I don't recall I did anything like that, how come?
3. In general how can I do that?

I know it is little bit long, I appreciate your time.

Thanks