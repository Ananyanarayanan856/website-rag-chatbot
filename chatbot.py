from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline

DB_DIRECTORY = "./website_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

db = Chroma(
    persist_directory=DB_DIRECTORY,
    embedding_function=embedding
)

# Local model
generator = pipeline(
    "text-generation",
    model="google/flan-t5-base",
    max_length=512
)

def retrieve_context(query: str, k: int = 3) -> str:
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])


def generate_answer(query: str, context: str) -> str:
    prompt = f"""
Answer the question ONLY using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""
    result = generator(prompt)[0]["generated_text"]
    return result


def chat(query: str) -> str:
    context = retrieve_context(query)
    return generate_answer(query, context)