import os
import boto3
from transformers import GPTJForCausalLM, GPT2Tokenizer
from supervisor_variables_aws import aws_configuration



# FYI: YOU SHOULD ONLY HAVE TO RUN THIS SCRIPT ONCE TO DOWNLOAD THE MODEL FROM HUGGING FACE USING ec2 AND SAVE IT TO THE S3 SYSTEM

# AWS configuration
AWS_ACCESS_KEY,AWS_SECRET_KEY,S3_BUCKET_NAME,MODEL_NAME,MODEL_DIR = aws_configuration()

# Initialize AWS S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Download the GPT-J model and tokenizer
def download_model():
    model = GPTJForCausalLM.from_pretrained(MODEL_NAME)
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    
    # Save the model and tokenizer locally
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

# Upload the model to S3
def upload_model_to_s3():
    for root, dirs, files in os.walk(MODEL_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            s3.upload_file(file_path, S3_BUCKET_NAME, f"{file}")  # Upload to root
            # print(f"Uploaded {file} to S3")

# Main function to download and upload the model
def main():
    download_model()
    upload_model_to_s3()

if __name__ == "__main__":
    main()
