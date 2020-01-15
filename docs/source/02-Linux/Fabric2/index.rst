Use Python Fabric boost your Development on Remote server 10 X easier
==============================================================================


What makes development on Remote Server difficult?
------------------------------------------------------------------------------

1. Edit long command in shell is hard.
2. Scripting in shell is hard, even though you are VIM master.
3. manage/upload/download artifacts interrupts your creativity, and hard to type commands.
4. MOST IMPORTANT: make your work repeatable and sync with your Git is HARD.


What is Fabric?
------------------------------------------------------------------------------

Fabric is a DevOps tool allow you to run shell commands, scripting, copy files via SSH.

Even better, it allows you to open a tunnel connect to jump host, and use your local computer like jump host. BUT, with your favorite GUI, text editor, shell which is not available on the jump host.

.. code-block:: python

    # -*- coding: utf-8 -*-
    from fabric2 import Connection

    with Connection(
        "ec2-111-111-111-111.compute-1.amazonaws.com",
        user="ec2-user",
        connect_kwargs=dict(
            key_filename=[
                Path(HOME, "my-ec2-pem", "eq-sanhe-dev.pem").abspath,
            ]
        )
    ) as conn:
        conn.run('yum -y install git')
        # and do more ...


Setup your Development Environment
------------------------------------------------------------------------------

TODO
