#!/usr/bin/env bash

cd ..
python3 -m build
python3 -m pip install --editable .
pytest