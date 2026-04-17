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
| **Data Scraping** | BeautifulSoup, Selenium, Custom Python Scripts |
| **Frontend** | HTML, CSS, JavaScript |

---

## ⚙️ How It Works

1. **Data Ingestion:** The scraper extracts URLs from a provided website sitemap and fetches the page contents.
2. **Vectorization:** The text is processed, split into manageable chunks, converted into embeddings, and stored locally in ChromaDB inside the chatbot's data folder.
3. **User Query:** The user enters a question into the web-based chat interface.
4. **Information Retrieval:** The backend converts the user's query into an embedding and retrieves the most relevant semantic chunks from the vector database.
5. **LLM Generation:** The retrieved data chunks are combined with the original query and passed to the Groq LLM as context.
6. **Response:** The chatbot returns a highly accurate, context-aware response to the user.

## 📂 Repository Structure

```text
website-rag-chatbot/
├── .env                        # Environment variables (create this)
├── chatbot/
│   ├── main.py                 # FastAPI backend entry point
│   ├── dataProcessing.py       # Text cleaning, chunking, and embedding logic
│   ├── requirements.txt        # Chatbot-specific dependencies
│   ├── data/                   # Generated folder containing the vector database
│   │   └── website_db/         # ChromaDB local storage
│   ├── static/
│   │   ├── script.js           # Frontend logic
│   │   └── style.css           # Frontend styling
│   └── templates/
│       └── index.html          # Chat interface structure
├── scraper/
│   ├── sitemap_extractor.py    # Sitemap extraction logic
│   ├── scraper.py              # Core scraping logic
│   └── run_scraper.py          # Script to execute the full scraping & embedding pipeline
├── .gitignore
├── README.md
├── requirements.txt            # Global project dependencies
└── setup_models.py             # Script to download TTS models
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

Run the following command to automatically prepare your environment:

```bash
make setup
```
> **Note:** Note: This command installs the required Python packages and pre-downloads the necessary AI models: `Faster-Whisper` (for speech-to-text) and `Piper TTS` (for text-to-speech). Once completed, the models will be cached locally for offline use.

### 4. Configure Environment Variables

Create a `.env` file in the root directory (or inside the `chatbot/` folder) and add your API keys:

```env
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
```
---

## ▶️ Running the Project

### Step 1: Run the Scraper Pipeline

> Optional — only required on the first run or when ingesting new website data.

```bash
cd scraper
python run_scraper.py
```

> **Note:** This will extract the sitemap, scrape the pages, and automatically call `dataProcessing.py` to build your vector database in `chatbot/data/website_db`.

### Step 2: Start the FastAPI Server

Open a new terminal (with the virtual environment active) and run:

```bash
cd chatbot
uvicorn main:app --reload
```

### Step 3: Open the Web Interface

Navigate to [http://localhost:8000](http://localhost:8000) in your browser to start chatting!