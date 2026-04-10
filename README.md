Website RAG Chatbot
Description

What it does: A production-ready AI chatbot designed to interact with users using context retrieved directly from a website's content.

Problem it solves: Prevents hallucination by grounding large language model (LLM) responses via accurate web scraping and vector search, ensuring users receive trustworthy, domain-specific information.

Key Idea: RAG-based chatbot for websites utilizing a dedicated scraping pipeline and local vector database.

Features
Chatbot interaction with a clean, responsive web-based interface
Website scraping and sitemap extraction pipeline
Retrieval-Augmented Generation (RAG) for accurate responses
FastAPI backend for high-performance APIs
ChromaDB vector database for similarity search
Tech Stack
Backend: Python, FastAPI, Uvicorn
AI/LLM: LangChain, Groq API, HuggingFace
Vector Database: ChromaDB
Frontend: HTML, CSS, JavaScript
Data Scraping: BeautifulSoup and custom Python scripts

website-rag-chatbot/
├── chatbot/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html
├── scraper/
│   ├── scraper.py
│   ├── run_scraper.py
│   └── dataProcessing.py
├── website_db/
├── .gitignore
├── README.md
└── requirements.txt


Installation and Setup
Clone the repository
git clone <repository-url>
cd website-rag-chatbot
Create a virtual environment
python -m venv venv
venv\Scripts\activate

For Linux or macOS

source venv/bin/activate
Install dependencies 
pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory (or inside the chatbot/ folder if specified) with the following keys:

HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key


Run the Project
Run the Scraper (Optional, if you need to ingest new data)
cd scraper
python run_scraper.py
Start the FastAPI Server
cd chatbot
uvicorn main:app --reload
Open the Web Interface
Navigate your browser to: http://localhost:8000


How It Works
1 Data Ingestion
   The scraper fetches pages from a website sitemap.
2 Vectorization
   Text is processed, split into chunks, converted into embeddings, and stored in ChromaDB.
3 User Query
   User enters a query in the chat interface.
4 Information Retrieval
   Backend converts the query into an embedding and retrieves relevant chunks from the vector database.
5 LLM Generation
   Retrieved data is combined with the query and sent to the Groq LLM.
6 Response
   The chatbot returns a context-aware response to the user.