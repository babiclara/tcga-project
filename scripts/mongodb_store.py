import os
import pandas as pd
from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://larababiicc:tcgaUser123@pppkcluster.63hxu.mongodb.net/?retryWrites=true&w=majority&appName=PPPKCluster"
DATABASE_NAME = "TCGA_DB"
COLLECTION_NAME = "GeneExpressions"

PROCESSED_DATA_DIR = "data/processed"

def store_to_mongodb():
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    for file in os.listdir(PROCESSED_DATA_DIR):
        if file.endswith(".tsv"):
            file_path = os.path.join(PROCESSED_DATA_DIR, file)
            df = pd.read_csv(file_path, sep='\t')
            records = df.to_dict(orient='records')
            collection.insert_many(records)
            print(f"Inserted {len(records)} records from {file} into MongoDB.")

    client.close()

if __name__ == "__main__":
    store_to_mongodb()
