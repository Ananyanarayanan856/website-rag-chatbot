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

    print("Extracting important text from JSON...")
    for item in scraped_items:
        url = item.get('url', 'Unknown URL')
        
        title = item.get('title', '')
        meta_desc = item.get('meta_description', '')
        paragraphs = item.get('paragraphs', [])
        
        # Combine the title, description, and paragraphs into one clean document
        content_parts = []
        if title:
            content_parts.append(f"Title: {title}")
        if meta_desc:
            content_parts.append(f"Description: {meta_desc}")
        if paragraphs:
            # Join all the paragraph strings together
            content_parts.extend(paragraphs)
            
        # Merge everything with double line breaks
        clean_text = "\n\n".join(content_parts)
        
        # Only add if there's actually text (some of your 404 pages have almost no text)
        if clean_text.strip():
            documents.append(Document(page_content=clean_text, metadata={"source": url}))

    print(f"Successfully extracted text from {len(documents)} pages.")
    
    if len(documents) == 0:
        print("ERROR: No documents processed. Something is wrong with the JSON structure.")
        return


 