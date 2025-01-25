import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

GENES_OF_INTEREST = [
    "C6orf150", "CCL5", "CXCL10", "TMEM173", "CXCL9",
    "CXCL11", "NFKB1", "IKBKE", "IRF3", "TREX1", "ATM", "IL6", "IL8"
]

def process_tsv_file(input_file, output_file):
    try:
        df = pd.read_csv(input_file, sep='\t', index_col=0)

        filtered_df = df[df.index.isin(GENES_OF_INTEREST)].T
        filtered_df["patient_id"] = filtered_df.index
        filtered_df["cancer_cohort"] = os.path.basename(input_file).split(".")[1]

        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        filtered_df.to_csv(output_file, sep='\t', index=False)
        print(f"Processed and saved: {output_file}")

    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_all_files():
    for file in os.listdir(RAW_DATA_DIR):
        if "HiSeqV2_PANCAN" in file:  
            input_path = os.path.join(RAW_DATA_DIR, file)
            output_path = os.path.join(PROCESSED_DATA_DIR, f"processed_{file}.tsv")
            process_tsv_file(input_path, output_path)

if __name__ == "__main__":
    process_all_files()
