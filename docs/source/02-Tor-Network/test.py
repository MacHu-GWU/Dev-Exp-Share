# -*- coding: utf-8 -*-

"""
Install these packages first:

.. code-block:: python

    pip install requests
    pip install pysocks
    pip install stem
"""

import time

import requests
from stem import Signal
from stem.control import Controller

RENEW_CONNECTION_WAIT_TIME = 5


def renew_connection():
    """
    Renew tor network connection (change route).
    """
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="mypassword")
        controller.signal(Signal.NEWNYM)
        controller.close()
    time.sleep(RENEW_CONNECTION_WAIT_TIME)


def make_session():
    """
    Make a session to keep connect
    """
    session = requests.session()
    session.proxies = {}
    session.proxies["http"] = "socks5h://localhost:9050"
    session.proxies["https"] = "socks5h://localhost:9050"
    return session


def check_ip():
    """
    Use Amazon Web Service to check your public IP.
    """
    session = make_session()
    url = "http://checkip.amazonaws.com/"
    return session.get(url).text


print(check_ip())
renew_connection()
print(check_ip())
