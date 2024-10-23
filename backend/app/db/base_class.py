from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseWithTimestamps(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), default=func.now(), onupdate=func.now()
    )
