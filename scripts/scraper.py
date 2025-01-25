import os
import requests
from tqdm import tqdm
import gzip
import shutil
CANCER_COHORTS = [
    {
      "Name": "TCGA Acute Myeloid Leukemia (LAML)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LAML.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Adrenocortical Cancer (ACC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.ACC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Bile Duct Cancer (CHOL)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.CHOL.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Bladder Cancer (BLCA)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.BLCA.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Breast Cancer (BRCA)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.BRCA.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Cervical Cancer (CESC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.CESC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Endometrioid Cancer (UCEC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.UCEC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Esophageal Cancer (ESCA)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.ESCA.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Glioblastoma (GBM)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.GBM.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Head and Neck Cancer (HNSC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.HNSC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Kidney Chromophobe (KICH)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.KICH.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Kidney Clear Cell Carcinoma (KIRC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.KIRC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Kidney Papillary Cell Carcinoma (KIRP)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.KIRP.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Kidney Clear Cell Carcinoma (KIRC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.KIRC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Large B-cell Lymphoma (DLBC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.DLBC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Liver Cancer (LIHC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LIHC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Lower Grade Glioma (LGG)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LGG.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Lung Adenocarcinoma (LUAD)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LUAD.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Lung Cancer (LUNG)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LUNG.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Lung Squamous Cell Carcinoma (LUSC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LUSC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Melanoma (SKCM)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.SKCM.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Mesothelioma (MESO)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.MESO.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Ocular melanomas (UVM)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.UVM.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Ovarian Cancer (OV)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.OV.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Pancreatic Cancer (PAAD)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.PAAD.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Pheochromocytoma & Paraganglioma (PCPG)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.PCPG.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Prostate Cancer (PRAD)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.PRAD.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Rectal Cancer (READ)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.READ.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Sarcoma (SARC)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.SARC.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Stomach Cancer (STAD)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.STAD.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Testicular Cancer (TGCT)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.TGCT.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Thymoma (THYM)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.THYM.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Thyroid Cancer (THCA)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.THCA.sampleMap%2FHiSeqV2_PANCAN.gz"
    },
    {
      "Name": "TCGA Uterine Carcinosarcoma (UCS)",
      "Url": "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.UCS.sampleMap%2FHiSeqV2_PANCAN.gz"
    }
  ]

DATA_DIR = "data/raw"

def download_and_extract_tsv_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    for cohort in CANCER_COHORTS:
        gz_filename = os.path.basename(cohort["Url"]).replace("%2F", "_")
        gz_file_path = os.path.join(DATA_DIR, gz_filename)
        tsv_file_path = gz_file_path.replace(".gz", "")

        print(f"Downloading data for {cohort['Name']}...")

        try:
            response = requests.get(cohort["Url"], stream=True)
            response.raise_for_status()

            with open(gz_file_path, "wb") as gz_file:
                for chunk in tqdm(response.iter_content(chunk_size=1024), desc=gz_filename, unit="KB"):
                    gz_file.write(chunk)

            print(f"Saved compressed file: {gz_file_path}")
            with gzip.open(gz_file_path, "rb") as f_in:
                with open(tsv_file_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            os.remove(gz_file_path) 
            print(f"Decompressed and saved: {tsv_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {cohort['Name']}: {e}")

if __name__ == "__main__":
    download_and_extract_tsv_files()