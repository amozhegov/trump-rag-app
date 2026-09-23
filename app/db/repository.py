from sqlalchemy.orm import Session

from db.models import QueryLog


def save_query(
    db: Session,
    *,
    keyword: str,
    found: bool,
    sentiment: str | None = None,
    transcript_excerpt: str | None = None,
    summary: str | None = None,
    message: str | None = None,
    search_ms: int | None = None,
    total_ms: int | None = None,
    error: str | None = None,
) -> QueryLog:
    row = QueryLog(
        keyword=keyword,
        found=found,
        sentiment=sentiment,
        transcript_excerpt=transcript_excerpt,
        summary=summary,
        message=message,
        search_ms=search_ms,
        total_ms=total_ms,
        error=error,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_recent_queries(db: Session, limit: int = 20) -> list[QueryLog]:
    return (
        db.query(QueryLog)
        .order_by(QueryLog.created_at.desc())
        .limit(limit)
        .all()
    )