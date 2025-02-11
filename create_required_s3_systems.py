import boto3
from botocore.exceptions import ClientError
from supervisor_variables_aws import aws_configuration


# FYI: SHOULD ONLY HAVE TO RUN SCRIPT ONCE TO CREATE REQUIURED S3 STORAGE SYSTEMS 

# AWS configuration
AWS_ACCESS_KEY,AWS_SECRET_KEY,S3_BUCKET_NAME,MODEL_NAME,MODEL_DIR = aws_configuration()

# AWS S3 client setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Define your S3 bucket name, can be what ever you want, make sure to change in superviro_variable.py script
bucket_name = S3_BUCKET_NAME

def create_s3_bucket_if_not_exists(bucket_name):
    try:
        # Check if the bucket already exists by listing all buckets
        response = s3.list_buckets()
        existing_buckets = [bucket['Name'] for bucket in response['Buckets']]

        if bucket_name in existing_buckets:
            ##print(f"Bucket '{bucket_name}' already exists.")
            pass
        else:
            # If the bucket does not exist, create it
            s3.create_bucket(Bucket=bucket_name)
            ##print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        pass
        ##print(f"Error occurred: {e}")

# Call the function to check and create the bucket

if __name__ == "__main__":
    create_s3_bucket_if_not_exists(bucket_name)
