import os
import json
import boto3
import torch
from transformers import pipeline
import fitz  # PyMuPDF for PDF text extraction
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import GPTJForCausalLM, GPT2Tokenizer
from supervisor_variables_aws import aws_configuration
from supervisor_variables_google import google_drive_variables
from user_query import user_query_prompt


GOOGLE_DRIVE_FILE_ID,PDF_FILE_NAME = google_drive_variables()

# AWS configuration
AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME, MODEL_NAME, MODEL_DIR = aws_configuration()

# Initialize AWS S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Download model from S3
def download_model_from_s3():
    """Download all model files from S3 to local directory"""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    model_files = ["pytorch_model.bin", "config.json", "tokenizer.json", "special_tokens_map.json"]
    
    for file in model_files:
        file_path = os.path.join(MODEL_DIR, file)
        try:
            s3.download_file(S3_BUCKET_NAME, file, file_path)
            #print(f"Downloaded {file} from S3.")
        except Exception as e:
            #print(f"Error downloading {file}: {e}")
            pass
    
    ##print(f"Model and tokenizer downloaded to {MODEL_DIR}")

# Load model
def load_model():
    """Load the GPT-J model and tokenizer properly from local storage."""
    try:
        if not os.path.exists(MODEL_DIR):
            raise FileNotFoundError(f"Model directory {MODEL_DIR} not found. Ensure the model is downloaded.")

        # Load tokenizer first
        tokenizer = GPT2Tokenizer.from_pretrained(MODEL_DIR)
        
        # Load model
        model = GPTJForCausalLM.from_pretrained(MODEL_DIR)
        
        # Move to GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        
        #print("Model and tokenizer loaded successfully.")
        return model, tokenizer
    except Exception as e:
        #print(f"Error loading model: {e}")
        return None, None

# PDF Processor to extract text and create FAISS index
class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text_chunks = self.extract_text()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Load once
        self.index, self.embeddings = self.create_faiss_index()

    def extract_text(self):
        """Extract text from the PDF and split into chunks"""
        doc = fitz.open(self.pdf_path)
        text_chunks = []
        for page in doc:
            text = page.get_text("text")
            text_chunks.extend(text.split("\n\n"))  # Split into meaningful sections
        return text_chunks

    def create_faiss_index(self):
        """Convert text into embeddings and store them in a FAISS index"""
        embeddings = np.array([self.model.encode(chunk) for chunk in self.text_chunks])
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, embeddings

    def search(self, query, top_k=3):
        """Retrieve the most relevant text chunks based on user query"""
        query_embedding = self.model.encode(query).reshape(1, -1)
        _, indices = self.index.search(query_embedding, top_k)
        return [self.text_chunks[i] for i in indices[0]]

# Function to download PDF from S3
def download_pdf_from_s3(pdf_filename):
    """Download PDF file from S3 bucket"""
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    s3.download_file(S3_BUCKET_NAME, pdf_filename, pdf_path)
    ##print(f"PDF file {pdf_filename} downloaded from S3.")
    return pdf_path

# Function to generate text using the model
def generate_text(model, tokenizer, prompt):
    """Generate text using the loaded model"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=200)
    
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Main function
def main():
    """Main script execution"""
    # Step 1: Download model from S3
    download_model_from_s3()
    
    # Step 2: Load the model and tokenizer
    model, tokenizer = load_model()
    if model is None or tokenizer is None:
        print("Failed to load the model. Exiting.")
        return

    # Step 3: Download the PDF from S3
    pdf_filename = PDF_FILE_NAME  # Adjust the filename
    pdf_path = download_pdf_from_s3(pdf_filename)
    
    # Step 4: Process the PDF
    pdf_processor = PDFProcessor(pdf_path)
    
    # Step 5: Handle user query
    user_query = user_query_prompt()
    retrieved_texts = pdf_processor.search(user_query)
    context_text = " ".join(retrieved_texts)

    # Step 6: Generate text based on extracted PDF content
    prompt = f"Based on this document: {context_text}\nAnswer the question: {user_query}"
    response = generate_text(model, tokenizer, prompt)
    
    # Step 7: Output the response
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
