# -*- coding: utf-8 -*-

import numpy
import pandas
import awswrangler
import scipy
import stumpy
import pynamodb

def handler(event, context):
    return {
        "numpy_version": numpy.__version__,
        "pandas_version": pandas.__version__,
        "awswrangler_version": awswrangler.__version__,
        "scipy_version": scipy.__version__,
        "stumpy_version": stumpy.__version__,
        "pynamodb_version": pynamodb.__version__,
    }
