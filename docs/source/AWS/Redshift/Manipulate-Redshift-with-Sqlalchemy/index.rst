Manipulate Redshift with Sqlalchemy
==============================================================================


DB Driver
------------------------------------------------------------------------------

Redshift is based on Postgresql, and the `psycopg2 <https://pypi.org/project/psycopg2>`_ is the most stable library to use.

``psycopy2`` is based on C, I highly recommend to use pre-compiled `psycopg2-binary <https://pypi.org/project/psycopg2-binary>`_ to replace ``pyscopy2``.

Redshift has some dialect. For example the `COPY <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html>`_ command. You need `sqlalchemy-redshift <https://pypi.org/project/sqlalchemy-redshift>`_ to enable those dialect.

**One problem**:

``sqlalchemy-redshift`` depends on ``psycopg2``, not ``psycopg2-binary``. In order to force install ``psycopg2-binary`` with ``sqlalchemy-redshift``, **you should put** ``sqlachemy-redshift`` **first, then** ``psycopg2-binary`` **in your** ``requirements.txt`` **file**.

::

    sqlachemy-redshift
    psycopg2-binary


COPY / UNLOAD Command with Sqlalchemy
------------------------------------------------------------------------------

Not only `COPY <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html>`_ and `UNLOAD <https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html>`_ Command, there's a lots of other DB Commands.

Sqlalchemy SQL Expression and ORM doesn't work for DB Command.

But Database Command is just a textual SQL:

.. code-block:: python


    from sqlalchemy import text

    stmt = text(
    """
    COPY users (id, name)
    FROM 's3://bucket-name/file-name.csv'
    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
    csv
    IGNOREHEADER 1
    """).execution_options(autocommit=True)
    engine.execute(stmt)

**Note**:

    Unlike standard sql statement, DB command doesn't do auto commit by default. You have to explicitly specified ``.execution_options(autocommit=True)``. Otherwise, no data will be uploaded in this example.

``UNLOAD`` Command is similar.


IAM Role
------------------------------------------------------------------------------

If your db command need to talk with other AWS Resource, you need an IAM Role to grant you access to do so. Although

For example, COPY / UNLOAD command requires an IAM Role to do so. If your need to talk to S3, the role you use has to have S3 access. If you need to talk to RDS, the role you use has to have RDS access.

You need to attach these IAM Role with your Redshift cluster first. `This article <https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-create-an-iam-role.html>`_ has some details.

**Create IAM Role to access other AWS Resource from Redshift**:

1. Go IAM console
2. Select type of trusted entity = Redshift -> Redshift - Customizable
3. If you want to talk to S3, attach S3 Policy (RDS and other resources is similar)
4. Go Redshift console, in iam roles menu, add the role you just create
5. Wait for "Modifying" to finish
