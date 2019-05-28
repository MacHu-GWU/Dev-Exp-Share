Connect via SSH
------------------------------------------------------------------------------

.. code-block:: bash

    $ ssh -i {path-to-your-pem-file} {username}@{ip-address}

- ``path-to-your-pem-file``:
- ``username``: the operation system username account. By default it is ``ec2-user``. It is not your IAM username!
- ``ip-address``: For EC2 on public subnet, public IPV4 address, can be found at your EC2 instances dashboard. For EC2 on private subnet, it is private IPV4 address.

Reference:

- Connecting to Your Linux Instance Using SSH: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
- Transferring Files to Linux Instances from Linux Using SCP


Copy file or dir between EC2 and local machien via SSH Copy
------------------------------------------------------------------------------

Reference:

- Linux – How to Securely Copy Files Using SCP examples: https://haydenjames.io/linux-securely-copy-files-using-scp/

.. code-block:: bash


    # Copy file from a EC2 to local host:
    $ scp -i {path-to-your-pem-file} <username>@<ec2-ip>:<path-to-ec2-file> <path-to-file>

    # Copy file from local host to a EC2:
    $ scp -i {path-to-your-pem-file} <path-to-file> <username>@<ec2-ip>:<path-to-ec2-file>


    # Copy directory from a EC2 to local host:
    $ scp -i {path-to-your-pem-file} -r <username>@<ec2-ip>:<path-to-ec2-dir> <path-to-dir>

    # Copy directory from local host to a EC2:
    $ scp -i {path-to-your-pem-file} -r <path-to-dir> <username>@<ec2-ip>:<path-to-ec2-dir>


chmod 400 ~/ec2-pem/ec2-lambda-deploy.pem
ssh -i ~/ec2-pem/ec2-lambda-deploy.pem ec2-user@35.168.23.253
ssh -i ~/ec2-pem/eqtest-sanhe.pem ec2-user@35.168.23.253

psql -h skymap-mpl-dev.cpe3safxwk8b.us-east-1.rds.amazonaws.com -d mpl -U skymap -e STZCXE!3u1c7