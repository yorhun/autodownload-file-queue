#!/bin/bash

python /home/pdf_downloader/tools/csv-to-mongo.py

cd /home/pdf_downloader/pdf_downloader
# Start the downloader
scrapy crawl downloader

tail -f /home/pdf_downloader/tools/empty.txt # keeps the container running for debugging if necesary

