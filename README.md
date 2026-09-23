# Trump RAG

Full-stack Retrieval-Augmented Generation (RAG) application that searches transcript chunks by keyword, classifies sentiment, and generates a Trump-style summary using local LLMs.

Dataset is availabale at:
https://www.kaggle.com/datasets/tangtaidje/donald-trump-rev-com-speech-transcripts-dataset

**Pipeline:** Keyword → vector search (Chroma) → sentiment classification → stylized summary (Ollama)

---

## Features

- Semantic search over transcript chunks with **keyword filtering** (improves relevance)
- **Sentiment classification** (`positive` / `negative`) via local LLM
- **Trump-style summary** (first person, ALL CAPS, few-shot prompting)
- **FastAPI** REST API (`POST /analyze`, `GET /health`)
- **React** frontend (Vite) for interactive queries
- **PostgreSQL** query history (SQLAlchemy)
- Environment-based configuration (`.env`)
- Application logging to console and `logs/app.log`
- Unit tests for retrieval filtering (`pytest`)
- Optional `start.sh` to launch API + frontend together

---

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | Python, FastAPI, Uvicorn, LangChain |
| Vector DB | ChromaDB |
| LLMs / Embeddings | Ollama (`nomic-embed-text`, `llama3.1:8b` / `qwen2.5`) |
| Database | PostgreSQL, SQLAlchemy |
| Frontend | React, Vite |
| Tooling | pytest, python-dotenv, logging |

---

## Project Structure

```text
app/
├── api/                 # FastAPI app, routes, schemas
├── rag/                 # retriever, summarizer, classifier, few-shot examples
├── embedding/           # Ollama embeddings
├── ingestion/           # document loading & chunking
├── vectorstore/         # Chroma helpers
├── db/                  # SQLAlchemy models, session, repository
├── frontend/            # React (Vite) UI
├── tests/               # unit tests
├── logs/                # app.log (gitignored)
├── chroma.db/           # vector store data (local)
├── config.py            # env-based settings
├── logging_config.py
├── ingest.py            # build / rebuild vector index
├── start.sh             # run API + frontend
├── .env.example
└── requirements.txt


## How retrieval works

Embed the keyword and run semantic search in Chroma (candidate_k, e.g. 30).
Filter chunks that actually contain the keyword (case-insensitive).
Return the top match(es) by semantic rank among filtered results.
Run sentiment classification on the transcript.
Generate a few-shot Trump-style summary grounded in the transcript and keyword.

Build the vector index
python ingest.py

Install dependencies
npm install

Running the app
chmod +x start.sh
./start.sh

Re-indexing (after changing documents, chunk size, or the embedding model):
python ingest.py