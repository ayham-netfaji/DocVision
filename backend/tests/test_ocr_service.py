import numpy as np

from app.services.ocr_service import OCRService


def test_ocr_service_init():
    service = OCRService()
    assert service is not None

def test_ocr_extract_text_interface():
    service = OCRService()
    # Create simple 200x200 image
    img = np.ones((200, 200), dtype=np.uint8) * 255
    res = service.extract_text(img)

    assert "text" in res
    assert "confidence" in res
    assert "word_count" in res
    assert "character_count" in res

def test_ocr_extract_text_mocked(monkeypatch):
    service = OCRService()
    # Mock is_available to True and pytesseract functions to verify parsing logic
    monkeypatch.setattr(service, "is_available", lambda: True)

    import pytesseract
    monkeypatch.setattr(
        pytesseract,
        "image_to_string",
        lambda img, config="": "HELLO DOCVISION TEST"
    )
    monkeypatch.setattr(
        pytesseract,
        "image_to_data",
        lambda img, output_type, config="": {
            "text": ["HELLO", "DOCVISION", "TEST"],
            "conf": [95, 98, 92]
        }
    )

    img = np.ones((100, 100), dtype=np.uint8) * 255
    res = service.extract_text(img)

    assert res["text"] == "HELLO DOCVISION TEST"
    assert res["word_count"] == 3
    assert res["confidence"] == 95.0
