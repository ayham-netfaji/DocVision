import io

from app.services.pdf_exporter import PDFExporter


def test_pdf_exporter_generates_bytes():
    exporter = PDFExporter()
    pdf_buffer = exporter.generate_pdf(
        document_id="test-doc-123",
        text="This is a DocVision automated unit test.\nOptical Character Recognition text.",
        confidence=96.4
    )

    assert isinstance(pdf_buffer, io.BytesIO)
    content = pdf_buffer.getvalue()
    assert len(content) > 0
    # PDF files must start with magic header %PDF-
    assert content.startswith(b"%PDF-")

def test_pdf_exporter_with_mock_image(tmp_path):
    from PIL import Image
    # Create temp image
    img_path = tmp_path / "test_scan.png"
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    img.save(img_path)

    exporter = PDFExporter()
    pdf_buffer = exporter.generate_pdf(
        document_id="test-img-doc",
        text="Sample paragraph with image embedded.",
        confidence=99.0,
        image_path=img_path
    )

    content = pdf_buffer.getvalue()
    assert content.startswith(b"%PDF-")
    assert len(content) > 1000
