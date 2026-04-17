import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os
import base64

# No need to add parent directory as text_to_speech is now local
from chatbot import chat
from text_to_speech import generate_speech
from urllib.parse import urlparse

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def get_company_name():
    website_url = os.environ.get("WEBSITE_URL", "")
    if not website_url:
        return "Website"
    
    parsed_url = urlparse(website_url)
    domain = parsed_url.netloc or parsed_url.path
    if domain.startswith("www."):
        domain = domain[4:]
    
    company_name = domain.split('.')[0]
    return company_name.capitalize()

app = FastAPI(title="AI Website Chatbot API")
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def home(request: Request):
    company_name = get_company_name()
    return templates.TemplateResponse(request=request, name="index.html", context={"company_name": company_name})

@app.post("/chat")
async def chat_endpoint(request_data: ChatRequest):
    user_query = request_data.query.strip()
    
    if not user_query:
        raise HTTPException(status_code=400, detail="No query provided")

    answer = chat(user_query)
    
    # Generate speech
    audio_base64 = None
    try:
        audio_bytes = generate_speech(answer)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print(f"TTS Error: {e}")
    
    return {"answer": answer, "audio": audio_base64}


if __name__ == "__main__":
    print("Starting FastAPI server...")
    # Triggering reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
