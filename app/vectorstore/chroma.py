from langchain_chroma import Chroma
#new
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

import time
#end new

def build_vectorstore(
    documents: list[Document],
    embeddings,
    persist_directory: str,
    batch_size: int = 32,
):
    print(f"Всего документов для индексации: {len(documents)}")
    
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )

    total_batches = (len(documents) + batch_size - 1) // batch_size

    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Батч {batch_num}/{total_batches} | чанки {i}–{min(i+batch_size, len(documents))}")

        # Простой retry при обрыве соединения
        for attempt in range(3):
            try:
                vectorstore.add_documents(batch)
                break
            except Exception as e:
                print(f"  Ошибка (попытка {attempt+1}/3): {e}")
                if attempt == 2:
                    raise
                time.sleep(3)

    print("Индексация завершена")
    return vectorstore

"""pip install langchain
pip install langchain-ollama
pip install langchain-chroma
pip install chromadb

И установить модель в Ollama:

ollama pull nomic-embed-text"""