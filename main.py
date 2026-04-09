from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sitemap_extractor import extract_urls
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/fetch", response_class=HTMLResponse)
def fetch_urls(request: Request):
    load_dotenv(override=True)
    website_url = os.getenv("WEBSITE_URL")
    if not website_url:
        result = {"urls": [], "error": "WEBSITE_URL is not set in .env file"}
    else:
        result = extract_urls(website_url)
        
        # Save the extracted URLs array to files for easy scraping
        if result.get("urls"):
            import json
            # Saving as JSON array
            with open("sitemap_urls.json", "w", encoding="utf-8") as f:
                json.dump(result["urls"], f, indent=4)
            # Saving as a Python variable (array) in a .py file
            with open("sitemap_data.py", "w", encoding="utf-8") as f:
                f.write(f"SITEMAP_URLS = {json.dumps(result['urls'], indent=4)}\n")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "urls": result["urls"],
            "error": result["error"]
        }
    )