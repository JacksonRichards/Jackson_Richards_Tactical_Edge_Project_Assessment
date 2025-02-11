AI-Powered Chatbot with PDF Integration and AWS Support
This repository contains a set of Python scripts that build a sophisticated AI-powered chatbot capable of processing and responding to queries based on PDF files stored in AWS S3. The system utilizes OpenAI's GPT-J model to generate responses and employs FAISS (Facebook AI Similarity Search) to retrieve the most relevant content from the PDFs.
The project is designed to run on an AWS EC2 instance with appropriate configuration for interacting with AWS S3 and Google Drive.
Overview of the Scripts
1. chatbot_initialization.py
•	Purpose: This script initializes the chatbot system by downloading the model and necessary files from AWS S3, processing PDF files stored in S3, extracting relevant content, and using GPT-J to generate answers based on user queries.
•	Key Components:
o	S3 Integration: Downloads model files and PDF from S3.
o	Model Loading: Loads the GPT-J model and tokenizer using Hugging Face's transformers library.
o	PDF Processing: Extracts and chunks text from PDF using PyMuPDF (fitz), then creates a FAISS index for efficient querying.
o	Query Handling: Accepts user queries, retrieves the most relevant text from the PDFs, and uses GPT-J to generate a response based on the extracted context.
o	Dependencies: boto3, torch, transformers, faiss, sentence-transformers, fitz.
2. create_required_s3_systems.py
•	Purpose: Sets up the necessary folders and directories in AWS S3 for storing models and other files required by the system.
•	Key Components:
o	S3 Bucket Creation: Initializes the required directory structure within an existing S3 bucket.
o	File Organization: Organizes model files, PDF files, and other resources needed by the chatbot.
•	Dependencies: boto3.
3. download_save_cloud_model.py
•	Purpose: Downloads the GPT-J model and tokenizer from Hugging Face and uploads them to AWS S3.
•	Key Components:
o	Model Download: Downloads the GPT-J model and tokenizer from Hugging Face.
o	Local Saving: Saves the model and tokenizer locally on the EC2 instance.
o	S3 Upload: Uploads the downloaded model files to a specified S3 bucket.
•	Dependencies: boto3, transformers.
4. supervisor_variables_aws.py
•	Purpose: Contains configuration variables for AWS, including credentials, bucket names, model names, and directories.
•	Key Components:
o	AWS Access: Provides the necessary AWS credentials (access key and secret key).
o	Bucket and Model Configurations: Specifies the names of the S3 bucket, the model name, and local directories for the model.
•	Dependencies: None. This script is purely configuration.
5. supervisor_variables_google.py
•	Purpose: Contains configuration variables related to Google Drive integration, such as the file ID for PDFs to be processed.
•	Key Components:
o	Google Drive Integration: Provides the file ID for accessing PDF files stored on Google Drive.
o	PDF Name: Specifies the name of the PDF file to be processed.
•	Dependencies: None. This script is purely configuration.
6. upload_pdf_file.py
•	Purpose: Uploads PDF files from a local system to an S3 bucket.
•	Key Components:
o	S3 Integration: Uploads the PDF file to the specified S3 bucket.
o	File Handling: Ensures the PDF file is transferred correctly.
•	Dependencies: boto3.
7. user_query.py
•	Purpose: Handles user input for querying the chatbot.
•	Key Components:
o	User Input: Accepts a query from the user and returns it for processing.
•	Dependencies: None.
8. README.md
•	Purpose: This file, which provides instructions, system architecture, and setup instructions for users.
________________________________________
Requirements
System Requirements
•	AWS EC2 Instance with an Ubuntu Linux operating system.
•	NVIDIA GPU (Optional): For faster processing with PyTorch and large language models like GPT-J.
•	Python 3.8+
Python Dependencies
pip install boto3 torch transformers faiss-cpu sentence-transformers PyMuPDF
AWS Configuration
Ensure that the EC2 instance has the appropriate AWS permissions:
1.	Create an IAM role with permissions to read/write to S3 and assign it to the EC2 instance.
2.	Store your AWS access and secret keys in the supervisor_variables_aws.py file.
Google Drive Integration (Optional)
If your PDFs are stored in Google Drive, set up the supervisor_variables_google.py file with the correct GOOGLE_DRIVE_FILE_ID.
________________________________________
Workflow
1. Download and Save the Model
Run the download_save_cloud_model.py script to download the GPT-J model and tokenizer from Hugging Face, save them locally, and then upload them to AWS S3. This step is required to store your model files in S3.
python download_save_cloud_model.py
2. Create Required S3 Systems
Once the model is uploaded, run the create_required_s3_systems.py script to set up the necessary directories in the S3 bucket for models and PDFs.
python create_required_s3_systems.py
3. Chatbot Initialization
The chatbot_initialization.py script ties everything together. It performs the following:
1.	Downloads the model and PDF from S3.
2.	Loads the model and tokenizer.
3.	Processes the PDF to extract relevant chunks of text.
4.	Accepts user queries and generates responses based on the extracted text using GPT-J.
To run the chatbot and process a query:
python chatbot_initialization.py
The system will:
•	Download the model and PDF from the S3 bucket.
•	Process the PDF and index its content using FAISS.
•	Generate a response based on a user query.
________________________________________
File Storage
1.	S3 Bucket Structure:
o	/models/gpt-j-6B/: Contains all model-related files (pytorch_model.bin, config.json, tokenizer.json, etc.).
o	/pdfs/: Store your PDF files that will be processed by the system.
2.	Local Directories:
o	MODEL_DIR: Where the model files are saved locally on the EC2 instance.
o	PDF_DIR: Directory where PDFs are temporarily downloaded and processed.
________________________________________
FAQ
1. How do I add more PDFs?
You can upload PDFs to the S3 bucket manually or use the upload_pdf_file.py script to upload PDF files from your local machine.
Example:
python upload_pdf_file.py <path-to-pdf> <s3-bucket-name> <destination-path>
2. How do I update the model?
To update the model, simply re-run the download_save_cloud_model.py script to download the latest version from Hugging Face and upload it to S3.
3. Can I run this on a local machine?
Yes, but the EC2 setup is optimized for cloud-based scaling and AWS S3 integration. If you run it locally, ensure that you have all dependencies set up and the required access to S3.

