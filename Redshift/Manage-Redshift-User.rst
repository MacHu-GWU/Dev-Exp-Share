Manage Redshift User
==============================================================================

**Important Concept**:

- `User <https://docs.aws.amazon.com/redshift/latest/dg/r_Users.html>`_: Single User
- `Group <https://docs.aws.amazon.com/redshift/latest/dg/r_Groups.html>`_: Group of Users
- `Schema <https://docs.aws.amazon.com/redshift/latest/dg/r_Schemas_and_tables.html>`_: Group of Tables

**Important Command**:

- `CREATE USER <https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_USER.html>`_ command: Create or Disable user (``CREATE USER username WITH PASSWORD DISABLE``)
- Privileges: list of operation allowed to operate
- `GRANT <https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html>`_ command: Grant specific user one or set of privilege
- `REVOKE <https://docs.aws.amazon.com/redshift/latest/dg/r_REVOKE.html>`_ command: inverse of GRANT
