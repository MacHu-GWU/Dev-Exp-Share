Use AWS Secret Manager to inject sensitive variable
==============================================================================

用 AWS Secret Manager 来管理敏感数据是一个很好的选择. ansible 内置了一个 aws.aws_secret 插件, 你只需要指定 secret 名称, 并且在你的运行环境中用 ``export AWS_DEFAULT_REGION="us-east-1"`` 制定了 region, 并且你的运行环境对应的 IAM Role 有足够的权限访问 AWS Secret. 那么你就可以将 secret data 的值 assign 给一个 variable, 然后再后面引用这个 variable.

对于复杂的 secret data, 建议使用 json 对数据进行编码, 以 plain text 的方式保存. 因为 ansible variable 系统基于 jinja2, ansible 实现了一个 json query 的 filter, 使用方式跟注明的 jq 命令一样. 从而可以访问复杂 json 数据结构中的某个具体的值.

我们看一个例子.

secret data::

    {
        "name": "alice",
        "tags": ["good person", "beauty"],
        "friends": [
            {"name": "bob"},
            {"name": "cathy"},
            {"name": "david"}
        ],
        "profile": {
            "ssn": "123-456-7890",
            "phone": "703-111-2222"
        }
    }

playbook::

    - name: action1
      hosts: all
      tasks:
      - name: Retrieve secrets from AWS Secrets Manager
        set_fact:
          secret_text: "{{ lookup('aws_secret', 'ansible-test') }}"
      - name: Print secrets
        debug:
          msg: "{{ secret_text }}"
      - name: Access complicate json data
        shell: |
          echo "{{ secret_text | json_query("name") }}"
          echo "{{ secret_text | json_query("profile.ssn") }}"
          echo "{{ secret_text | json_query("tags[0]") }}"
          echo "{{ secret_text | json_query("friends[1].name") }}"

而如果你需要有足够的权限来访问某个具体的 secret, 你最少需要这些 IAM Policy::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": "arn:aws:secretsmanager:us-east-1:${aws_account}:secret:${secret_name_and_surfix}"
            }
        ]
    }

参考资料:

- https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_secret_lookup.html
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#selecting-json-data-json-queries