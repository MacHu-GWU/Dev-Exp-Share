#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Install these package first::

    pip install requests
    pip install pysocks
"""

import time
import requests

session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

st = time.clock()
url = "https://www.python.org"
r = session.get(url) # it could be slower using tor
# print(r.text)
print(time.clock() - st)

# try with onion network only wetsite
# r = session.get("http://httpbin.org/ip")
# print(r.text)

# r = session.get("https://www.facebookcorewwwi.onion/")
# print(r.text)