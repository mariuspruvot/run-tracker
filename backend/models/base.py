from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
# With Base declared here : alembic can autogenerate migrations because it will resolve the path by importing
# __init__.py and finding Base there
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
