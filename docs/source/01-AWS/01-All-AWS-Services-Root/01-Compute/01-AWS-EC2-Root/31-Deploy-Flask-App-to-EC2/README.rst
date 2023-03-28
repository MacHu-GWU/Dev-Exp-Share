Deploy Flask App to EC2
==============================================================================


Web App 的基础概念
------------------------------------------------------------------------------

一个 Webapp 本质上就是一台将他的 http = 80, https = 443 端口向公网世界开放的电脑. 而在这台电脑上运行着一个 http 服务器. http 服务器的实现方式有非常多种, 简直数不过来.

在 flask 中使用的是 wsgi http server.


一个极简的运行在 EC2 上的 Flask Web 服务器
------------------------------------------------------------------------------

1. 需要一个 VPC, 拥有一个 Public Subnet
2. 在 Public Subnet 上启动一个 EC2, 最好使用 amazon linux, 因为 amazon linux 预装 python
3. 给这个 EC2 配置 Security Group, 其中必须开放用于 HTTP 的 TCP 80 端口, 以及用于 SSH 的 TCP 端口
4. SSH 到你的虚拟机, 先安装 ``pip``, ``flask``:

.. code-block:: bash

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python get-pip.py
    sudo pip install flask

5. 然后创建一个 ``app.py`` 文件, 填入以下内容:

.. code-block:: bash

    touch app.py
    vim app.py

.. code-block:: python

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

6. 用 flask 命令行启动服务器:

.. code-block:: python

    sudo flask run -h 0.0.0.0 -p 80

7. 现在你可以从公网用浏览器访问这个网站了 http://ec2-111-111-111-111.compute-1.amazonaws.com
