# -*- coding: utf-8 -*-

"""
this script is to send http request to the web app server
"""

import requests

host = "http://127.0.0.1:36737"
url_delete_all = f"{host}/delete_all"
url_plus_one = f"{host}/plus_one"

# Delete all
# res = requests.get(url_delete_all)
# print(res.status_code)
# print(res.text)

# This would work
res = requests.post(url_plus_one, data={"key": "k1"})
print(res.status_code)
print(res.text)

# This won't work
# res = requests.get(url_plus_one)
# print(res.status_code)
# print(res.text)

# This won't work
# res = requests.post(url_plus_one, data={"invalid_key": 123})
# print(res.status_code)
# print(res.text)
