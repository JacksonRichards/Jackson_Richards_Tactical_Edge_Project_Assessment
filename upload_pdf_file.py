import os
import gdown
import boto3
from supervisor_variables_aws import aws_configuration
from supervisor_variables_google import google_drive_variables

# AWS configuration
AWS_ACCESS_KEY,AWS_SECRET_KEY,S3_BUCKET_NAME,MODEL_NAME,MODEL_DIR = aws_configuration()

# Initialize AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Google Drive file ID (the part after /d/ and before /view)
GOOGLE_DRIVE_FILE_ID, PDF_FILE_NAME = google_drive_variables()

# Construct the download URL for Google Drive
download_url = f'https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}'

# Download the file using gdown
gdown.download(download_url, PDF_FILE_NAME, quiet=False)

# Upload the file to S3
def upload_to_s3():
    try:
        # Upload the file to S3
        s3.upload_file(PDF_FILE_NAME, S3_BUCKET_NAME, PDF_FILE_NAME)
        ##print(f'File successfully uploaded to {S3_BUCKET_NAME} as {PDF_FILE_NAME}')
    except Exception as e:
        pass
        ##print(f'Error uploading file: {e}')

# Run the upload function
if __name__ == "__main__":
    upload_to_s3()

