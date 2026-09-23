from config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

from ingestion.loader import load_data
from ingestion.preprocessing import split_documents

from embedding.embedder import get_embeddings
from vectorstore.chroma import build_vectorstore

from config import CHROMA_PATH

#from embedding.embedder import create_embeddings
#from vectorstore.chroma import save_embeddings

#одна и та же модель должна использоваться и для индексации, и для поиска.

#Benchmark example = (Model Text Embedding Benchmark)

#0llama + chroma + langchain (nomic-embed-text)

"""Ollama — локальная модель эмбеддингов (bge-m3 или nomic-embed-text);
Chroma — локальное хранение и поиск векторов;
Document — как стандартный контейнер данных;
RecursiveCharacterTextSplitter — если документы большие."""

"""documents = load_data(DATA_PATH)


chunks = split_documents(
    documents,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
print("chunks are done")
print('chunks len =', len(chunks))"""



"""print(len(chunks))
print(len(documents))
chunk = chunks[0]
print(chunk.page_content)
print('Meta:')
print(chunk.metadata)
print('-------')
print(chunks[0])"""

"""embeddings = create_embeddings(chunks)


save_embeddings(
    chunks,
    embeddings
)"""

#new code

"""embeddings = get_embeddings()
print("embeddings are done")

from embedding.embedder import get_embeddings
emb = get_embeddings()
vec = emb.embed_documents(["тестовый текст для проверки"])
print(len(vec[0]))

db = build_vectorstore(
    documents = chunks,
    embeddings = embeddings,
    persist_directory=CHROMA_PATH,
)
print("vectorstore is done")"""

# main.py
from langchain_chroma import Chroma
from embedding.embedder import get_embeddings
from config import CHROMA_PATH

def main():
    embeddings = get_embeddings()

    # Просто загружаем готовую базу
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )

    print(f"База загружена. Документов: {db._collection.count()}")


if __name__ == "__main__":
    main()