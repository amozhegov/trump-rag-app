import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from embedding.embedder import get_embeddings
from config import CHROMA_PATH

logger = logging.getLogger(__name__)

def get_vectorstore() -> Chroma:
    #Get previously indexed embeddings
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings(),
    )

#def get_retriever(k: int = 1):
def get_retriever(k: int = 20):
    #returns retriever (by default return 1 document)
    db = get_vectorstore()
    return db.as_retriever(search_kwargs={'k':k})

def search(query: str, 
           k: int = 1,
           candidate_k: int = 30,
           require_keyword: bool = True,
           ) -> list[Document]:
    'Gets keyword, returns a list of found documents'
    retriever = get_retriever(k=candidate_k)
    docs = retriever.invoke(query)
    if not require_keyword:
        return docs[:k]
    query_lower = query.lower().strip()
    filtered = [
        doc for doc in docs
        if query_lower in doc.page_content.lower()
    ]
    logger.info(
    "retriever | query=%r | candidates=%d | after_filter=%d | return=%d",
    query,
    len(docs),
    len(filtered),
    len(filtered[:k]),
    )
    #return retriever.invoke(query)
    return filtered[:k]

