import os
import boto3

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "admin123"
BUCKET_NAME = "tcga-data"
DOWNLOAD_DIR = "data/downloaded"

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

def download_files_from_minio():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            file_name = obj['Key']
            download_path = os.path.join(DOWNLOAD_DIR, file_name)
            
            s3_client.download_file(BUCKET_NAME, file_name, download_path)
            print(f"Downloaded {file_name} to {download_path}")
    else:
        print("No files found in the bucket.")

if __name__ == "__main__":
    download_files_from_minio()
