

Connect to SSH::

    EC2_IP="111.111.111.111" # assign the IP to this var
    ssh -i ~/ec2-pem/eq-sanhe-dev.pem "ec2-user@$EC2_IP"

::

    ansible all -i host.yml -m ping

Test ansible playbook::

    ansible-playbook -i host.yml playbook.yml --extra-vars "@vars.yml"
    ansible-playbook -i host.yml playbook.yml --extra-vars "@vars.json"