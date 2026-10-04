import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db import crud

@pytest.fixture
def test_db_session():
    # In-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()

def test_create_and_get_document(test_db_session):
    doc = crud.create_document_record(
        db=test_db_session,
        doc_id="test_db_1",
        filename="invoice.jpg",
        original_path="/uploads/test_db_1.jpg",
        processed_path="/uploads/test_db_1_processed.png",
        text="INVOICE #9821 TOTAL: $450",
        confidence=98.7,
        word_count=4,
        char_count=26
    )

    assert doc.id == "test_db_1"
    assert doc.ocr_result is not None
    assert doc.ocr_result.confidence == 98.7
    assert doc.ocr_result.text == "INVOICE #9821 TOTAL: $450"

    # Query all
    docs = crud.get_all_documents(test_db_session)
    assert len(docs) == 1
    assert docs[0].id == "test_db_1"

    # Query single
    fetched = crud.get_document_by_id(test_db_session, "test_db_1")
    assert fetched is not None
    assert fetched.filename == "invoice.jpg"

    # Delete
    deleted = crud.delete_document_by_id(test_db_session, "test_db_1")
    assert deleted is True
    assert crud.get_document_by_id(test_db_session, "test_db_1") is None
