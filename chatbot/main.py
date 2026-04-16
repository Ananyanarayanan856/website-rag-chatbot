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

# Add the parent directory to sys.path so we can import text_to_speech
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from chatbot import chat
from text_to_speech import generate_speech

app = FastAPI(title="AI Website Chatbot API")
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def home(request: Request):
 
    return templates.TemplateResponse(request=request, name="index.html")

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
