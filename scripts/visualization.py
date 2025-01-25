import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://larababiicc:tcgaUser123@pppkcluster.63hxu.mongodb.net/?retryWrites=true&w=majority&appName=PPPKCluster"
DATABASE_NAME = "TCGA_DB"
COLLECTION_NAME = "GeneExpressions"

GENES = ["IRF3", "TMEM173", "CXCL11", "CXCL10", "CXCL9", "IL6", "IL8", 
         "ATM", "NFKB1", "TREX1", "CCL5", "C6orf150", "IKBKE"]

def visualize_gene_expression(gene):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    data = collection.find({}, {gene: 1, "patient_id": 1, "_id": 0})
    df = pd.DataFrame(data)

    if df.empty:
        print(f"No data found for gene {gene}")
        return

    plt.figure(figsize=(12, 6))
    plt.bar(df['patient_id'], df[gene], color='blue')
    plt.xlabel('Patient ID')
    plt.ylabel(f'{gene} Expression')
    plt.title(f'{gene} Gene Expression Across Patients')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def visualize_all_genes():
    for gene in GENES:
        visualize_gene_expression(gene)

if __name__ == "__main__":
    visualize_all_genes()
