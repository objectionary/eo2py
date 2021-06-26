#!/usr/bin/env bash

cd ..
rm -rf dist
python3 -m build
twine upload --verbose --repository eo2py dist/*
echo "> Waiting until upload finishes..."
sleep 12s
echo "> Installing the new version of eo2py..."
python3 -m pip install --upgrade eo2py
