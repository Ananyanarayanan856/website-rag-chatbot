import os
from dotenv import load_dotenv
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
    If the answer is not in the context, say "I can help you with company related informations.Thank You!".
    
    Context:
    {context}
    
    Question:
    {query}
    """
    
    result = llm.invoke(prompt)
    return result.content

def chat(query: str) -> str:
    print(f"\nUser: {query}")
    context = retrieve_context(query)
    answer = generate_answer(query, context)
    return answer

#  Test
if __name__ == "__main__":
    while 1:
        test_question=input("Enter the question: ")
        response = chat(test_question)
        print(f"\nBot: {response}\n")