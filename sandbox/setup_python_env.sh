#!/usr/bin/env bash

if ! [[ -e "venv" ]]; then
  echo "Python virtual environment (venv) doesn't exist in $(pwd), creating one..." && sleep 1s
  python -m venv venv
fi

echo "Activating venv.." && sleep 1s
source venv/bin/activate
which python && sleep 1s

echo "Installing dependencies..." && sleep 1s
python -m pip install black ../eo-python-runtime/
cd .. && mvn -DskipTests clean install
cd sandbox || exit
