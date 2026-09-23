from langchain_chroma import Chroma
from embedding.embedder import get_embeddings
from config import CHROMA_PATH

# Загружаем уже готовую базу
embeddings = get_embeddings()

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)

print(f"Количество документов в Chroma: {db._collection.count()}")

# Берём один любой документ
result = db._collection.get(limit=1)

print("\n" + "="*50)
print("ID:", result["ids"][0])
print("Метаданные:", result["metadatas"][0])
print("\nТекст:")
print(result["documents"][0])
print("="*50)