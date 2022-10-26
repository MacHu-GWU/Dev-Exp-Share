#!/bin/bash

virtualenv -p python3.8 .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip freeze
