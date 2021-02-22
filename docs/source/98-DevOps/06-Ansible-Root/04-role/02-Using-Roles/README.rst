
From official docs https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#using-roles

You can use roles in three ways:

1. at the play level with the roles option: This is the classic way of using roles in a play.
2. at the tasks level with ``include_role``: You can reuse roles dynamically anywhere in the tasks section of a play using include_role.
3. at the tasks level with ``import_role``: You can reuse roles statically anywhere in the tasks section of a play using import_role.
