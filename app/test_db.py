from langchain_chroma import Chroma
from embedding.embedder import get_embeddings
from config import CHROMA_PATH

embeddings = get_embeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

print("Total docs:", db._collection.count())

result = db._collection.get(limit=2)
print("\nID:", result["ids"][1])
print("Metadata:", result["metadatas"][1])
print("\Text:\n", result["documents"][1][:1000])