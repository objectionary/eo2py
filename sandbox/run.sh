#!/usr/bin/env bash

echo "Activating venv..." && sleep 1s
source venv/bin/activate

echo "Compiling .eo files..." && sleep 1s
cd .. && mvn clean install
cd sandbox || exit
mvn clean compile

echo "Generated Python Files:" && sleep 1s
ls  target/generated-sources/

echo "Formatting python files with black..." && sleep 1s
printf "\n\nif __name__ == \"__main__\":\n    print(EOapp().dataize().data())\n\n" >> target/generated-sources/app.eo.py
python -m black $(find target/generated-sources | sed -n '2, $p' | tr '\n' ' ')

echo "Running Python files..." && sleep 1s
python target/generated-sources/app.eo.py

echo "Deactivating venv..." && sleep 1s
deactivate
