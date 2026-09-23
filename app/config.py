from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to app/.env "
        "(see .env.example)."
    )

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Trump_Labeled_Combined_Rev_Speeches_Final_9-24-2024.json"

#reduce CHUNK_SIZE=500,
#reduce CHUNK_OVERLAP=100,
CHUNK_SIZE=1000,
CHUNK_OVERLAP=200,

#Is it necessary?
EMBEDDING_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma.db")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3.1:8b")
#EMBEDDING_MODEL = "nomic-embed-text"
#CHROMA_PATH = './chroma.db'

