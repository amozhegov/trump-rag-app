# ingest.py
from config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_PATH

from ingestion.loader import load_data
from ingestion.preprocessing import split_documents
from embedding.embedder import get_embeddings
from vectorstore.chroma import build_vectorstore

def main():
    print("Загрузка документов...")
    documents = load_data(DATA_PATH)

    print("Разбиение на чанки...")
    chunks = split_documents(
        documents,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    print(f"Чанков: {len(chunks)}")

    print("Создание эмбеддингов и сохранение в Chroma...")
    embeddings = get_embeddings()

    db = build_vectorstore(
        documents=chunks,
        embeddings=embeddings,
        persist_directory=CHROMA_PATH,
        batch_size=16,
    )

    print(f"Готово. Документов в базе: {db._collection.count()}")

if __name__ == "__main__":
    main()