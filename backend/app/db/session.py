from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()