### Automated queue to download files

#### Uses scrapy, pandas, and mongodb to set up a download queue from a list of file urls

##### "url-suffixes.csv" defines the urls to be visited. This file needs to be created by user in the path "/pdf_downloader/data/pdf-strings/url-suffixes.csv", the remaining process is automatized after running docker compose:

1. After running docker compose, a download queue is created in the form of MongoDB collection (the queue is made up of url substrings specified in "url-suffixes.csv", these should be prepared beforehand)
2. Using this queue, scrapy downloads files located in the urls, the download delay can be adjusted in /pdf_downloader/pdf_downloader/settings.py to not overload a server
3. Using mongodb queue, download status of the queue is tracked by the download_status field (10 for downloaded, 1,2,3... for storing attempted download count, 0 for those not attempted), this way, if a file download is incomplete, scrapy will attempt to download it again after the rest of the queue is finished.
