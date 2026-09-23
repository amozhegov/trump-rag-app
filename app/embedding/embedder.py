#from model import model

"""def create_embeddings(chunks):
    return model.encode(chunks).tolist()"""
"""
def create_embeddings(documents):

    texts = [
        doc.page_content
        for doc in documents
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()"""

from langchain_ollama import OllamaEmbeddings

def get_embeddings():
    return OllamaEmbeddings(
        model = 'nomic-embed-text',
        #base_url='http://localhost:11434'
    )