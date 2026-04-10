import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq


load_dotenv()
hf_token = os.getenv("HF_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")

if not hf_token:
    raise ValueError("HF_TOKEN not found!")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found!")

DB_DIRECTORY = "./website_db"

print("Loading Database and Embeddings...")
embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)

db = Chroma(
    persist_directory=DB_DIRECTORY,
    embedding_function=embedding
)

print("Connecting to Groq API...")
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=groq_api_key,
    temperature=0.3 
)

def retrieve_context(query: str, k: int = 3) -> str:
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])

def generate_answer(query: str, context: str) -> str:
    prompt = f"""
    Answer the question ONLY using the provided context.
    If the answer is not in the context, say "I can help you with company related informations. Thank You!".
    
    Context:
    {context}
    
    Question:
    {query}
    """
    
    result = llm.invoke(prompt)
    return result.content


app = FastAPI(title="AI Website Chatbot API")


templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def home(request: Request):
 
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request_data: ChatRequest):
    user_query = request_data.query.strip()
    
    if not user_query:
        raise HTTPException(status_code=400, detail="No query provided")

    print(f"\nUser: {user_query}")
    context = retrieve_context(user_query)
    answer = generate_answer(user_query, context)
    print(f"Bot: {answer}\n")
    
    return {"answer": answer}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)