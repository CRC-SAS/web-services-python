#!/usr/bin/env bash

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install wheel
python -m pip install setuptools
python -m pip install jupyterlab
python -m pip install Cython
