import os
import boto3

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "admin123"
BUCKET_NAME = "tcga-data"

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

PROCESSED_DATA_DIR = "data/processed"

def upload_files_to_minio():
    for file in os.listdir(PROCESSED_DATA_DIR):
        if file.endswith(".tsv"):
            file_path = os.path.join(PROCESSED_DATA_DIR, file)
            try:
                s3_client.upload_file(file_path, BUCKET_NAME, file)
                print(f"Successfully uploaded {file} to {BUCKET_NAME}")
            except Exception as e:
                print(f"Failed to upload {file}: {e}")

if __name__ == "__main__":
    upload_files_to_minio()
