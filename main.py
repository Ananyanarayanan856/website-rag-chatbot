from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from sitemap_extractor import extract_urls
from chatbot import chat  # ✅ Added chatbot import

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# -------------------------------
# Home Route
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


# -------------------------------
# Sitemap Fetch Route
# -------------------------------
@app.post("/fetch", response_class=HTMLResponse)
def fetch_urls(request: Request):
    load_dotenv(override=True)
    website_url = os.getenv("WEBSITE_URL")

    if not website_url:
        result = {"urls": [], "error": "WEBSITE_URL is not set in .env file"}
    else:
        result = extract_urls(website_url)

        # Save extracted URLs
        if result.get("urls"):
            import json
            with open("sitemap_urls.json", "w", encoding="utf-8") as f:
                json.dump(result["urls"], f, indent=4)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "urls": result.get("urls", []),
            "error": result.get("error")
        }
    )


# -------------------------------
# Chat API (JSON)
# -------------------------------
class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chatbot_api(request: ChatRequest):
    answer = chat(request.query)
    return {"answer": answer}


# -------------------------------
# Chat UI (Form-based)
# -------------------------------
@app.post("/ask", response_class=HTMLResponse)
def ask_question(request: Request, query: str = Form(...)):
    answer = chat(query)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "answer": answer
        }
    )