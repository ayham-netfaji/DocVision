import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ocr_status():
    response = client.get("/api/v1/ocr/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_scan_document_valid_image():
    # Create a dummy JPEG image in memory
    fake_image = io.BytesIO(b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"\x00" * 100)
    response = client.post(
        "/api/v1/documents/scan",
        files={"image": ("test_doc.jpg", fake_image, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "completed"
    assert data["confidence"] > 0

def test_scan_document_invalid_extension():
    fake_txt = io.BytesIO(b"Hello text document")
    response = client.post(
        "/api/v1/documents/scan",
        files={"image": ("test.txt", fake_txt, "text/plain")}
    )
    assert response.status_code == 400
