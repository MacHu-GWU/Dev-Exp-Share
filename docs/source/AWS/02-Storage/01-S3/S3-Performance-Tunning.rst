.. _s3-add-hex-hash-key-as-prefix:

Add Hex Hash of the Key as Prefix to evenly Distribute the requests traffic
==============================================================================

First, very important, S3 is not a hierarchy structured storage, it is simply a key value. The ``/`` only gives you a logical directory view of the objects.

Internally, S3 shard objects based on the first few character of the Key (full absolute path, except the bucket name).

If you are doing a Facebook-like application where users will upload lots of images. To avoid overwhelming number of read and write request on the S3 Bucket, a trick can be used is use hex hash of the key as prefix, usually first few characters (4-6) is enough.

For example, if your key looks like::

    s3://<bucket>/2013-06-25/cust1234/photo1.jpg
    s3://<bucket>/2013-06-25/cust1234/photo2.jpg
    s3://<bucket>/2013-06-25/cust1234/photo3.jpg

you should use ``hash("2013-06-25/cust1234/photo1.jpg")`` = "6b0a", then you use::

    s3://<bucket>/6b0a-2013-06-25/cust1234/photo1.jpg
    ...

If you don't do this, requests for same days' photo will go to the same S3 shard. It could be: today shard A takes 90% of the traffic, tomorrow shard B takes 90% of the traffic.

By adding prefix, it evenly distribute the traffic.

In order to get all photos in a post, or all photos uploaded by a user, you should put this information in your database.
