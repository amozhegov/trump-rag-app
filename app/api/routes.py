import logging
import time

from fastapi import APIRouter, HTTPException

from api.schemas import AnalyzeRequest, AnalyzeResponse
from rag.retriever import search
from rag.classifier import classify_sentiment
from rag.summarizer import summarize_transcript
from db.session import SessionLocal
from db.repository import save_query

router = APIRouter()
logger = logging.getLogger(__name__)


def _safe_save(**kwargs):
    """Сохранить в Postgres; сбой БД только в лог."""
    db = SessionLocal()
    try:
        save_query(db, **kwargs)
    except Exception:
        logger.exception("failed to save query log to postgres")
    finally:
        db.close()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is empty")

    t0 = time.perf_counter()
    logger.info("analyze started | keyword=%r", keyword)

    search_ms = None
    try:
        t_search = time.perf_counter()
        docs = search(keyword, k=1)
        search_ms = int((time.perf_counter() - t_search) * 1000)
    except Exception as e:
        logger.exception("search failed | keyword=%r", keyword)
        total_ms = int((time.perf_counter() - t0) * 1000)
        _safe_save(
            keyword=keyword,
            found=False,
            error=str(e),
            search_ms=search_ms,
            total_ms=total_ms,
        )
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

    if not docs:
        total_ms = int((time.perf_counter() - t0) * 1000)
        msg = "Nothing found for this keyword"
        logger.info("analyze empty | keyword=%r | total_ms=%d", keyword, total_ms)
        _safe_save(
            keyword=keyword,
            found=False,
            message=msg,
            search_ms=search_ms,
            total_ms=total_ms,
        )
        return AnalyzeResponse(keyword=keyword, found=False, message=msg)

    transcript = docs[0].page_content
    excerpt = transcript[:1200] + ("..." if len(transcript) > 1200 else "")

    sentiment = None
    summary = None
    error_parts = []

    try:
        sentiment = classify_sentiment(transcript)
    except Exception as e:
        logger.exception("classify failed | keyword=%r", keyword)
        sentiment = f"error: {e}"
        error_parts.append(f"classify: {e}")

    try:
        summary = summarize_transcript(transcript, query=keyword)
    except Exception as e:
        logger.exception("summarize failed | keyword=%r", keyword)
        summary = f"error: {e}"
        error_parts.append(f"summarize: {e}")

    total_ms = int((time.perf_counter() - t0) * 1000)
    logger.info("analyze done | keyword=%r | total_ms=%d", keyword, total_ms)

    _safe_save(
        keyword=keyword,
        found=True,
        sentiment=sentiment,
        transcript_excerpt=excerpt,
        summary=summary,
        search_ms=search_ms,
        total_ms=total_ms,
        error="; ".join(error_parts) if error_parts else None,
    )

    return AnalyzeResponse(
        keyword=keyword,
        found=True,
        transcript_excerpt=excerpt,
        sentiment=sentiment,
        summary=summary,
    )