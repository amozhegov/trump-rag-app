from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import DATABASE_URL

class Base(DeclarativeBase):
    # Base Class for table models
    pass
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping = True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    from db.models import QueryLog
    Base.metadata.create_all(bind = engine)

