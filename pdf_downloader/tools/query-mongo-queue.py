#/usr/bin/env python3

# Description: This script queries the queue-collection in the queue-db database,
# Returns the percentage of documents where download_status = 10
# Can be called from host machine

# import pandas and pymongo
import pandas as pd
from pymongo import MongoClient, ASCENDING

# Connect to MongoDB

client = MongoClient('mongodb://localhost:27020')

db = client['queue-db']
collection = db['queue-collection']

# Query the collection for documents where download_status  = 10

query = {'download_status': 10}
cursor = collection.find(query)
cursor = list(cursor)
# print the number of documents in the cursor divided by total doc count * 100 (%)

print(f"{len(cursor) / collection.count_documents({}) * 100:.2f}% of documents have download_status = 10")

client.close()