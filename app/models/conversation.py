from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID as PyUUID
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, func
from datetime import datetime


class Conversation(Base):
    __tablename__ = 'conversations'
    # <typehint for sqlalchemy> = <value type for postgres>

    # PyUUID is a typehint, UUID is postgres column and uuid.4 as function creating UUID value
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(String(255), nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=True)
    confidence: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())