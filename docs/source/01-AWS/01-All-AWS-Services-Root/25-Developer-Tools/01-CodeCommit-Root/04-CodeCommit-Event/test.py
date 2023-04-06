# -*- coding: utf-8 -*-

import os
import pytest
import json
from pathlib import Path




if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
