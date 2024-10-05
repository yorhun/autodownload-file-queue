#/usr/bin/env python3

# import pandas and pymongo
import pandas as pd
from pymongo import MongoClient, ASCENDING

# Connect to MongoDB

client = MongoClient('mongodb://localhost:27020')

# Create a database and a collection

db = client['queue-db']

# Create a collection
print("Creating collection 'queue-collection'")
collection = db['queue-collection']


csv_path = "/home/pdf_downloader/data/pdf-strings/url-suffixes.csv"

# Read the CSV file
print("Reading CSV file")
df = pd.read_csv(
    csv_path,
    dtype = str
    )

df['download_status'] = 0 # 0 for not attempted, 10 for downloaded, +1 for each download attempt up to 9 attempts
print(df)
# Convert the DataFrame to a dictionary and insert to mongo collection



df_dict = df.to_dict(orient='records')

print("Inserting data to collection")
collection.insert_many(df_dict)

# index collection on 'download_status' field
print("Creating index on 'download_status' field")
collection.create_index([('download_status', ASCENDING)])
# Close the connection

client.close()