# -*- coding: utf-8 -*-

import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import jsonpickle.ext.pandas as jsonpickle_pandas

jsonpickle_numpy.register_handlers()
jsonpickle_pandas.register_handlers()
jsonpickle.set_encoder_options("simplejson", sort_keys=True)

import attr
import numpy as np
import pandas as pd
from datetime import datetime


class User:
    def __init__(self, name):
        self.name = name


@attr.s
class Account:
    username = attr.ib()
    password = attr.ib()


dct = dict(
    a_str="hello world!",
    a_int=100,
    a_float=3.14,
    a_bool=True,
    a_bytes="hello world!".encode("utf-8"),
    a_datetime=datetime.now(),
    a_user_object=User(name="Alice"),
    a_account_object=Account(username="alice@example.com", password="mypassword"),
    a_numpy_array=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
    a_pandas_dataframe=pd.DataFrame([("a", 1), ("b", 2)], columns=["alpha", "number"]),
)

print(dct)
ser_dct = jsonpickle.dumps(dct, indent=4)

print(type(ser_dct))
print(ser_dct)

deser_dct = jsonpickle.loads(ser_dct)
print(deser_dct)
