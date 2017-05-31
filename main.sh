#!/bin/bash
cd ifeve
if [ ! -f "ifeve.db" ]
then
    scrapy crawl ifeve
    scrapy crawl body
fi
cd ..
python3.5 ifeveFlask.py