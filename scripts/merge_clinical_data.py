import pandas as pd
import os

EXPRESSION_DATA_DIR = "data/processed"
CLINICAL_FILE_PATH = "data/processed/TCGA_clinical_survival_data.tsv"
OUTPUT_DIR = "data/merged"

os.makedirs(OUTPUT_DIR, exist_ok=True)

CLINICAL_COLUMNS = ["bcr_patient_barcode", "DSS", "OS", "clinical_stage"]

def merge_gene_expression_with_clinical(expression_file):
    df_expr = pd.read_csv(expression_file, sep='\t')
    
    if "patient_id" not in df_expr.columns:
        raise ValueError(f"Missing 'patient_id' column in {expression_file}")

    df_clinical = pd.read_csv(CLINICAL_FILE_PATH, sep='\t', usecols=CLINICAL_COLUMNS)

    merged_df = pd.merge(df_expr, df_clinical, left_on="patient_id", right_on="bcr_patient_barcode", how="inner")

    merged_df.drop(columns=["bcr_patient_barcode"], inplace=True)

    output_file = os.path.join(OUTPUT_DIR, os.path.basename(expression_file).replace("processed_", "merged_"))
    merged_df.to_csv(output_file, sep='\t', index=False)

    print(f"Merged data saved to {output_file}")

if __name__ == "__main__":
    for file in os.listdir(EXPRESSION_DATA_DIR):
        if file.endswith(".tsv"):
            expression_file_path = os.path.join(EXPRESSION_DATA_DIR, file)
            try:
                merge_gene_expression_with_clinical(expression_file_path)
            except Exception as e:
                print(f"Error processing {file}: {e}")
