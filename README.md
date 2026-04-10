# 🤖 Website RAG Chatbot

> A production-ready AI chatbot designed to interact with users using context retrieved directly from a website's content.

## 📖 Overview

The Website RAG Chatbot prevents large language model (LLM) hallucinations by grounding responses via accurate web scraping and vector search. By utilizing a dedicated scraping pipeline and a local vector database, it ensures users receive trustworthy, domain-specific information directly from the source.

**Key Idea:** A Retrieval-Augmented Generation (RAG) chatbot utilizing a dedicated data ingestion pipeline and a robust local vector database.

---

## ✨ Features

- **Clean Web Interface:** A responsive and intuitive chat interface for seamless user interaction.
- **Automated Scraping Pipeline:** Custom website scraping and sitemap extraction to ingest the latest content.
- **Retrieval-Augmented Generation (RAG):** Context-aware, accurate, and hallucination-free AI responses.
- **High-Performance Backend:** Built on FastAPI for rapid and efficient API endpoints.
- **Similarity Search:** Powered by ChromaDB for lightning-fast vector retrieval.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Backend** | Python, FastAPI, Uvicorn |
| **AI / LLM** | LangChain, Groq API, HuggingFace |
| **Vector Database** | ChromaDB |
| **Data Scraping** | BeautifulSoup, Custom Python Scripts |
| **Frontend** | HTML, CSS, JavaScript |

---

## ⚙️ How It Works

1. **Data Ingestion:** The scraper fetches pages from a provided website sitemap.
2. **Vectorization:** The text is processed, split into manageable chunks, converted into embeddings, and stored locally in ChromaDB.
3. **User Query:** The user enters a question into the web-based chat interface.
4. **Information Retrieval:** The backend converts the user's query into an embedding and retrieves the most relevant semantic chunks from the vector database.
5. **LLM Generation:** The retrieved data chunks are combined with the original query and passed to the Groq LLM as context.
6. **Response:** The chatbot returns a highly accurate, context-aware response to the user.

---

## 📂 Repository Structure

```text
website-rag-chatbot/
├── chatbot/
│   ├── main.py                 # FastAPI backend entry point
│   ├── requirements.txt        # Chatbot-specific dependencies
│   ├── .env                    # Environment variables (create this)
│   ├── static/
│   │   ├── script.js           # Frontend logic
│   │   └── style.css           # Frontend styling
│   └── templates/
│       └── index.html          # Chat interface structure
├── scraper/
│   ├── scraper.py              # Core scraping logic
│   ├── run_scraper.py          # Script to execute the scraping pipeline
│   └── dataProcessing.py       # Text cleaning and chunking utilities
├── website_db/                 # ChromaDB local storage (generated)
├── .gitignore
├── README.md
└── requirements.txt            # Global project dependencies
```

---

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ananyanarayanan856/website-rag-chatbot.git
cd website-rag-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Running the Project

### Step 1: Run the Scraper

> Optional — only required on the first run or when ingesting new website data.

```bash
cd scraper
python run_scraper.py
```

### Step 2: Start the FastAPI Server

Open a new terminal (with the virtual environment active) and run:

```bash
cd chatbot
uvicorn main:app --reload
```

### Step 3: Open the Web Interface

Navigate to [http://localhost:8000](http://localhost:8000) in your browser to start chatting!