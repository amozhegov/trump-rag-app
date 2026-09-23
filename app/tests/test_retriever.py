from types import SimpleNamespace
from unittest.mock import patch

from langchain_core.documents import Document

from rag.retriever import search

def make_docs():
    return [
        Document(page_content="Speech about Italy and trade deals."),
        Document(page_content="Speech about France and borders."),
        Document(page_content="Another mention of italy in lowercase."),
        Document(page_content="Nothing relevant here."),
    ]

class FakeRetriever:
    def __init__(self, docs):
        self._docs = docs

    def invoke(self, query):
        return self._docs

def test_require_keyword_filters_docs():
    docs = make_docs()
    with patch('rag.retriever.get_retriever', return_value = FakeRetriever(docs)):
        result = search('Italy', k = 5, candidate_k = 10, require_keyword = True)

        assert len(result) == 2
        assert all("italy" in d.page_content.lower() for d in result)
        # порядок сохраняется: сначала более "верхний" из семантического списка
        assert "Italy and trade" in result[0].page_content

def test_require_keyword_respects_k():
    docs = make_docs()

    with patch("rag.retriever.get_retriever", return_value = FakeRetriever(docs)):
        result = search("Italy", k = 1, candidate_k = 10, require_keyword = True)

    assert len(result) == 1
    assert "italy" in result[0].page_content.lower()


def test_no_matches_returns_empty_list():
    docs = make_docs()

    with patch("rag.retriever.get_retriever", return_value = FakeRetriever(docs)):
        result = search("Brazil", k = 3, candidate_k = 10, require_keyword = True)

    assert result == []


def test_require_keyword_false_returns_top_k_without_filter():
    docs = make_docs()

    with patch("rag.retriever.get_retriever", return_value = FakeRetriever(docs)):
        result = search("Italy", k = 2, candidate_k = 10, require_keyword = False)

    assert len(result) == 2
    assert result[0].page_content == docs[0].page_content
    assert result[1].page_content == docs[1].page_content


def test_keyword_is_case_insensitive_and_stripped():
    docs = [
        Document(page_content="Talk about ITALY today."),
    ]

    with patch("rag.retriever.get_retriever", return_value = FakeRetriever(docs)):
        result = search("  italy  ", k = 1, candidate_k = 5, require_keyword = True)

    assert len(result) == 1