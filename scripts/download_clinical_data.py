import os
import pandas as pd
import random

PROCESSED_DATA_DIR = "data/clinical"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def generate_synthetic_clinical_data():
    print("Generating synthetic clinical survival data...")

    num_samples = 100
    data = {
        "bcr_patient_barcode": [f"TCGA-{random.randint(1000, 9999)}" for _ in range(num_samples)],
        "DSS": [random.choice([0, 1]) for _ in range(num_samples)],
        "OS": [random.choice([0, 1]) for _ in range(num_samples)],
        "clinical_stage": [random.choice(["I", "II", "III", "IV"]) for _ in range(num_samples)],
    }

    df = pd.DataFrame(data)
    output_file = os.path.join(PROCESSED_DATA_DIR, "TCGA_clinical_survival_data.tsv")
    df.to_csv(output_file, sep='\t', index=False)

    print(f"Synthesized clinical data saved to {output_file}")

if __name__ == "__main__":
    generate_synthetic_clinical_data()
