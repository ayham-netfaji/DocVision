
from sqlalchemy.orm import Session

from app.db.models import Document, OCRResult


def create_document_record(
    db: Session,
    doc_id: str,
    filename: str,
    original_path: str,
    processed_path: str | None = None,
    text: str = "",
    confidence: float = 0.0,
    word_count: int = 0,
    char_count: int = 0
) -> Document:
    doc = Document(
        id=doc_id,
        filename=filename,
        status="completed",
        original_image_path=original_path,
        processed_image_path=processed_path
    )
    db.add(doc)

    ocr = OCRResult(
        document_id=doc_id,
        text=text,
        confidence=confidence,
        word_count=word_count,
        character_count=char_count
    )
    db.add(ocr)

    db.commit()
    db.refresh(doc)
    return doc


def get_all_documents(db: Session, limit: int = 50, offset: int = 0) -> list[Document]:
    return db.query(Document).order_by(Document.created_at.desc()).offset(offset).limit(limit).all()


def get_document_by_id(db: Session, doc_id: str) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()


def delete_document_by_id(db: Session, doc_id: str) -> bool:
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
        return True
    return False
