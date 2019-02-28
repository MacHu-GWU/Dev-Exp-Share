Copy Command


Reference:

- Copy Command: https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html
- Copy Command Examples: https://docs.aws.amazon.com/redshift/latest/dg/r_COPY_command_examples.html


Understand Copy Command
------------------------------------------------------------------------------

A copy command tells Redshift:

- load to which table, which columns? you can custom column mapping.
- from where? s3 / database / others ..., a single file? a folder?
- authorization to perform this command, use either IAM or API Key
- data format? csv / json / parquet ...
- data format specified options, such as ``gzip``, ``IGNOREHEADER 1`` ...


Work with CSV File
------------------------------------------------------------------------------

Data for ``table.users``::

    id,name
    1,Alice
    2,Bob
    3,Cathy


Command::

    COPY users (id, name)
    FROM 's3://<bucket-name>/<data-file-key>'
    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
    csv
    IGNOREHEADER 1;

You can replace::

    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'

with::

    access_key_id 'AAAAAAAAAAAAAAAAAAAA'
    secret_access_key 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


If it is gzip compressed::

    COPY users (id, name)
    FROM 's3://<bucket-name>/<data-file-key>'
    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
    csv
    IGNOREHEADER 1
    gzip;
