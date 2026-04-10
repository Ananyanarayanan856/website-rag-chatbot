import json
import os
from dotenv import load_dotenv  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.documents import Document

load_dotenv()

def process_scraped_data(json_file_path, db_directory="./website_db"):
    print(f"Loading data from {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as file:
        scraped_items = json.load(file)

    documents = []

    print("Extracting important text from JSON...")
    for item in scraped_items:
        url = item.get('url', 'Unknown URL')
        title = item.get('title', '')
        meta_desc = item.get('meta_description', '')
        paragraphs = item.get('paragraphs', [])
        
        content_parts = []
        if title:
            content_parts.append(f"Title: {title}")
        if meta_desc:
            content_parts.append(f"Description: {meta_desc}")
        if paragraphs:
            content_parts.extend(paragraphs)
            
        clean_text = "\n\n".join(content_parts)
        
        if clean_text.strip():
            documents.append(Document(page_content=clean_text, metadata={"source": url}))

    print(f"Successfully extracted text from {len(documents)} pages.")
    
    if len(documents) == 0:
        print("No documents processed. Something is wrong with the JSON structure.")
        return
 
    print("Chunking the text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")
    
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token:
        print("HF_TOKEN not found")
        return

    print("Connecting to Hugging Face API for embeddings...")
    
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=hf_token
    )
    
    print("Embedding chunks via API and saving to vector database...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_directory 
    )

    print(f"Success! Vector database saved locally at: {db_directory}")

if __name__ == "__main__":
    process_scraped_data('scraped_data.json')