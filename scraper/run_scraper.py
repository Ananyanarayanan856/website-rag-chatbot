import os
import json
import sys

# Ensure the working directory is strictly this folder so paths don't glitch
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Add the chatbot directory to Python's path
chatbot_dir = os.path.abspath(os.path.join(current_dir, "..", "chatbot"))
sys.path.append(chatbot_dir)

# Import local modules
from sitemap_extractor import extract_urls
import scraper  
from dataProcessing import process_scraped_data 

def main():
    print("=== Website RAG Chatbot Scraper Pipeline ===")
    base_url = input("Enter the base URL of the website to scrape (e.g., https://example.com): ").strip()
    
    if not base_url:
        print("URL cannot be empty. Exiting.")
        return

    # Step 1: Extract URLs from sitemap
    print("\n--- Step 1: Extracting URLs from Sitemap ---")
    result = extract_urls(base_url)
    if result["error"]:
        print(f"[ERROR] Failed to extract URLs: {result['error']}")
        return
        
    unique_urls = result["urls"]
    print(f"Found {len(unique_urls)} unique URLs.")
    
    # Save the urls to sitemap_urls.json
    sitemap_file = "sitemap_urls.json"
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        json.dump(unique_urls, f, indent=4)
    print(f"Saved extracted URLs to {sitemap_file}")

    # Step 2: Scrape the pages
    print("\n--- Step 2: Scraping Pages ---")
    scraper.main()  # This uses sitemap_urls.json and writes to data.json

    # Step 3: Process the data into the Chromadb vector database
    print("\n--- Step 3: Processing Data into Vector Database ---")
    
    data_folder_path = os.path.join("..", "chatbot", "data")
    db_path = os.path.join(data_folder_path, "website_db")
    
    # Ensure the 'data' folder actually exists before we try to save inside it
    os.makedirs(data_folder_path, exist_ok=True)
    # --------------------------------------------------------------
    
    scraped_file = "data.json" 
    
    if not os.path.exists(scraped_file):
        print(f"[ERROR] {scraped_file} not found. Scraping might have failed.")
        return
        
    process_scraped_data(scraped_file, db_directory=db_path)
    
    print("\n=== Pipeline Complete! ===")
    print(f"The vector database has been saved to: {os.path.abspath(db_path)}")
    print("You can now run 'python main.py' from the chatbot folder to start the AI server.")

if __name__ == "__main__":
    main()