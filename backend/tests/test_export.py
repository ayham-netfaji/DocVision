from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_export_pdf_endpoint():
    response = client.get(
        "/api/v1/export/sample-doc-123/pdf",
        params={"text": "Export testing paragraph line 1\nLine 2", "confidence": 98.2}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == 'attachment; filename="DocVision_sample-doc-123.pdf"'
    assert response.content.startswith(b"%PDF-")
