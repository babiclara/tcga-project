import os
import pandas as pd

PROCESSED_DATA_DIR = "data/processed"
CLINICAL_FILE_PATH = "data/clinical/TCGA_clinical_survival_data.tsv"
OUTPUT_DIR = "data/merged"

os.makedirs(OUTPUT_DIR, exist_ok=True)

CLINICAL_COLUMNS = ["bcr_patient_barcode", "DSS", "OS", "clinical_stage"]

def merge_gene_expression_with_clinical(processed_file):
    print(f"Processing {processed_file}...")

    df_expr = pd.read_csv(processed_file, sep='\t')

    if "patient_id" not in df_expr.columns:
        print(f"Error: 'patient_id' column missing in {processed_file}")
        return

    df_clinical = pd.read_csv(CLINICAL_FILE_PATH, sep='\t', usecols=CLINICAL_COLUMNS)

    df_expr["patient_id"] = df_expr["patient_id"].str.split('-').str[:3].str.join('-').str.upper().str.strip()
    df_clinical["bcr_patient_barcode"] = df_clinical["bcr_patient_barcode"].str.upper().str.strip()

    print(f"Gene expression patients: {df_expr['patient_id'].nunique()} patients")
    print(f"Clinical data patients: {df_clinical['bcr_patient_barcode'].nunique()} patients")

    merged_df = pd.merge(df_expr, df_clinical, left_on="patient_id", right_on="bcr_patient_barcode", how="inner")

    if merged_df.empty:
        print(f"Warning: No matching patient records found for {processed_file}")
    else:
        merged_df = merged_df[[
            "IRF3", "TMEM173", "CXCL11", "CXCL10", "CXCL9", "IL6", "IL8", "ATM", "NFKB1", "TREX1", "CCL5", "C6orf150", "IKBKE",
            "patient_id", "cancer_cohort", "clinical_stage", "OS", "DSS"
        ]]

        output_file = os.path.join(OUTPUT_DIR, os.path.basename(processed_file).replace("processed_", "merged_"))
        merged_df.to_csv(output_file, sep='\t', index=False)
        print(f"Merged data saved to {output_file}")

if __name__ == "__main__":
    if not os.path.exists(CLINICAL_FILE_PATH):
        print(f"Error: Clinical data file '{CLINICAL_FILE_PATH}' not found.")
        exit(1)

    files_found = [f for f in os.listdir(PROCESSED_DATA_DIR) if f.endswith(".tsv")]
    if not files_found:
        print("No processed TSV files found in the 'data/processed' directory.")
    else:
        print(f"Found {len(files_found)} processed TSV files. Starting merging...")

    for file in files_found:
        processed_file_path = os.path.join(PROCESSED_DATA_DIR, file)
        try:
            merge_gene_expression_with_clinical(processed_file_path)
        except Exception as e:
            print(f"Error processing {file}: {e}")
