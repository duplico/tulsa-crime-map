#!/bin/bash

cd /home/george/project/tulsa-crime-map
#source `which virtualenvwrapper.sh`
source /usr/local/bin/virtualenvwrapper.sh
workon crimemap
runzeo --pid-file zeo.pid -C zeo.config &
scrapy crawl crimemap
python parse_fire.py

