from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), default="completed")
    original_image_path = Column(String(500), nullable=False)
    processed_image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationship to OCR Results
    ocr_result = relationship("OCRResult", back_populates="document", uselist=False, cascade="all, delete-orphan")


class OCRResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    word_count = Column(Integer, default=0)
    character_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationship back to Document
    document = relationship("Document", back_populates="ocr_result")
