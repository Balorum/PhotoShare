from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings


def create_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def get_db():
    engine = create_engine("sqlite:///./test.db")
    db = None
    try:
        db = create_session(engine)
        yield db
    finally:
        if db is not None:
            db.close()
