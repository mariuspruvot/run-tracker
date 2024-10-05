from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped
import uuid
from backend.models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    username: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)
