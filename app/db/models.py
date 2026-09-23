from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class QueryLog(Base):
    __tablename__ = "queries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    keyword: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    found: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sentiment: Mapped[str | None] = mapped_column(String(64), nullable=True)
    transcript_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    message: Mapped[str | None] = mapped_column(String(512), nullable=True)
    search_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)