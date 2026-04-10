import re
import json
import os
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

def get_sitemap_url(base_url):
    """Constructs the sitemap URL from the base URL."""
    return urljoin(base_url, "/sitemap.xml")

def extract_urls(base_url):
    """Uses Selenium to fetch and parse URLs from a sitemap.xml file."""
    sitemap_url = get_sitemap_url(base_url)
    print(f"--- Fetching sitemap from: {sitemap_url} ---")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        driver.get(sitemap_url)
        
        time.sleep(2)
        
        page_source = driver.page_source
        
        # Regex to find all <loc>...</loc> tags
        urls = re.findall(r'<loc[^>]*>\s*(.*?)\s*</loc>', page_source, re.IGNORECASE)
        
        # Check for 404s if no URLs found
        if not urls:
            if "404" in driver.title or "Not Found" in driver.title:
                 return {"error": f"404 Client Error: Not Found for url: {sitemap_url}", "urls": []}

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(urls))
        return {"error": None, "urls": unique_urls}
        
    except Exception as e:
        return {"error": str(e), "urls": []}
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # 1. Try to get URL from .env first, otherwise ask for user input
    target_url = os.getenv("WEBSITE_URL")
    
    if not target_url:
        target_url = input("Enter the website URL (e.g., https://example.com): ").strip()

    if target_url:
        result = extract_urls(target_url)

        if result["error"]:
            print(f"Error: {result['error']}")
        else:
            url_list = result["urls"]
            print(f"Successfully extracted {len(url_list)} URLs.")

            # 2. Save to JSON file (Same logic as your previous main.py)
            if url_list:
                output_file = "sitemap_urls.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(url_list, f, indent=4)
                print(f"Results saved to {output_file}")
            else:
                print("No URLs were found in the sitemap.")
    else:
        print("No URL provided. Exiting.")