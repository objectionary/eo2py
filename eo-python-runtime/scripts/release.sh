#!/usr/bin/env bash

cd ..
rm -rf dist
python3 -m build
# TODO: bump version
#echo "Enter the part of the version you want to update: "
#read version_part
#if [[ "$version_part" == "major" || "$version_part" == "minor" || "$version_part" == "patch" ]]; then
#  bump2version
#fi
twine upload --verbose --repository eo2py dist/*
echo "> Waiting until upload finishes..."
sleep 12s
echo "> Installing the new version of eo2py..."
python3 -m pip install --upgrade eo2py
