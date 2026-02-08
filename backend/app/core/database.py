"""Database connection and session management"""
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from app.core.config import DATABASE_URL, connect_args, ENVIRONMENT

engine = create_engine(
    DATABASE_URL,
    echo=ENVIRONMENT == "development",  # Log SQL queries in development
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=20,
    max_overflow=10
)

def get_session() -> Generator[Session, None, None]:
    """Dependency to provide a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)