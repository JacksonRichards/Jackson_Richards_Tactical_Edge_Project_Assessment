
def aws_configuration():
    AWS_ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # s3 key
    AWS_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # s3 secret key
    S3_BUCKET_NAME = "jackson-richards-technical-assessment-tacticaledge"
    MODEL_NAME = "EleutherAI/gpt-j-6B"  # Model you want to use Default: EleutherAI/gpt-j-6B
    MODEL_DIR = r"C:\Users\Administrator\gpt-j-model"  # Adjust the path based on your system and User
    return(AWS_ACCESS_KEY,AWS_SECRET_KEY,S3_BUCKET_NAME,MODEL_NAME,MODEL_DIR)