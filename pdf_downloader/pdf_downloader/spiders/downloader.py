import scrapy
import pandas as pd
import os
from glob import glob
from pymongo import MongoClient

class DownloaderSpider(scrapy.Spider):
    name = 'downloader'

    # init
    def __init__(self):
        client = MongoClient('mongodb://localhost:27020')
        db = client['queue-db']
        collection = db['queue-collection']

        N = 1
        # get N documents from the collection where download_status < 9
        # if all works well, N can be removed and all documents can be downloaded

        iteration_list = pd.DataFrame(list(collection.find({'download_status': {'$lt': 9}}).limit(N)))
        client.close()

        downloaded_files = glob('/home/pdf_downloader/container-data/*/*.pdf')
        downloaded_files = [f.split('/')[-1].split('.')[0] for f in downloaded_files]

        # filter iteration list for files not already downloaded
        iteration_list = iteration_list[~iteration_list['url-suffixes'].isin(downloaded_files)]
        print("Will download {} files".format(len(iteration_list)))

        iteration_list = iteration_list.sample(frac=1)
        self.full_code_list = iteration_list['url-suffixes'].tolist()
        self.folder_list = iteration_list['url-suffixes'].str[:6].tolist()


        ##########################################################
        ## this part should be adapted to the website structure ##
        ##########################################################

        repeating_url_prefix = ''
        suffix = iteration_list['url-suffixes'].str[:6] + "/" + iteration_list['url-suffixes']

        # prefix for the url may be the main part of url like www.example.com/pdfs
        # the joined suffixes constitute the rest of the url like 123456.pdf
        # should be adapted according to the website structure

        self.pdf_links = repeating_url_prefix + suffix + '.pdf'
        self.mongo_ids = iteration_list['_id'].tolist()

    def start_requests(self):
        for i, url in enumerate(self.pdf_links):
            yield scrapy.Request(
                url=url,
                callback=self.save_pdf,
                meta = {
                    'folder': self.folder_list[i],
                    'full_code': self.full_code_list[i],
                    'mongo_id': self.mongo_ids[i],
                    'scraped_url': url
                }
            )

    def save_pdf(self, response):

        folder_path = '/home/pdf_downloader/container-data/pdf-files/' + response.meta['folder']

        client = MongoClient('mongodb://localhost:27020')
        db = client['queue-db']
        collection = db['queue-collection']

        # increase the download status by 1 (attempt registers as +1 to download_status whether successful or not)
        collection.update_one({'_id': response.meta['mongo_id']}, {'$inc': {'download_status': 1}})

        # Check if the folder exists
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
        # define paths
        pdf_path = folder_path + "/" + response.meta['full_code'] + ".pdf"
        if not os.path.isfile(pdf_path):
        # Perform a Python command, for example, creating the file
            with open(pdf_path, 'wb') as f:
                f.write(response.body)
            print(f"File '{pdf_path}' created.")

            # set the download status to 10 (meaning downloaded)
            collection.update_one({'_id': response.meta['mongo_id']}, {'$set': {'download_status': 10}})

        client.close()
