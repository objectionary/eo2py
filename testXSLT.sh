#!/usr/bin/bash
cd /home/nikololiahim/IdeaProjects/eo-runtime-python || exit
mvn clean install
cd sandbox || exit
mvn clean compile
gedit target/05-compile/app.eo.xml &
gedit target/04-pre/app.eo.xml/??-pre-data.xml &
