import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import chat


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
    
    return {"answer": answer}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    # Triggering reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
