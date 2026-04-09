import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

def process_scraped_data(json_file_path, db_directory="./website_db"):
    print(f"Loading data from {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as file:
        scraped_items = json.load(file)

    documents = []

 