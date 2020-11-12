

ssh -i ~/ec2-pem/eq-sanhe-dev.pem ec2-user@3.87.112.144


ansible all -i host.yml -m ping

ansible-playbook -i host playbook.yml