# попробовать убрать polarity subjectivity из metadata

import json
from langchain_core.documents import Document

def load_data(path: str) -> list[Document]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    documents = []

    for i in data["transcript"]:
        documents.append(
            Document(
                page_content=data["transcript"][i],
                metadata={
                    "title": data["title"][i],
                    "date": data["date"][i],
                    "link": data["link"][i],
#                    "word_count": data["word_count"][i],
#                   "polarity": data["polarity"][i],
#                  "subjectivity": data["subjectivity"][i],
                }
            )
        )
    return documents