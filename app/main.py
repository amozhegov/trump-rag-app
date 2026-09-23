from config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

from ingestion.loader import load_data
from ingestion.preprocessing import split_documents

from embedding.embedder import get_embeddings
from vectorstore.chroma import build_vectorstore

from config import CHROMA_PATH

# main.py
from langchain_chroma import Chroma
from embedding.embedder import get_embeddings
from config import CHROMA_PATH

def main():
    embeddings = get_embeddings()

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )

    print(f"DB is loaded. Number of Docs: {db._collection.count()}")


if __name__ == "__main__":
    main()