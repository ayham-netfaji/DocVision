import io
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from app.core.config import settings
from app.services.pdf_exporter import PDFExporter

router = APIRouter()

@router.get("/{document_id}/pdf")
async def export_document_pdf(
    document_id: str,
    text: Optional[str] = Query(None),
    confidence: Optional[float] = Query(95.0)
):
    """
    Generates and streams a formatted PDF export for a processed document.
    """
    # Check for processed image on disk
    processed_path = settings.upload_dir / f"{document_id}_processed.png"
    if not processed_path.exists():
        # Fallback to original image if processed image not present
        matches = list(settings.upload_dir.glob(f"{document_id}.*"))
        processed_path = matches[0] if matches else None

    # Load text from session parameter or fallback placeholder
    extracted_text = text or f"DocVision Document {document_id}\n\nProcessed with Computer Vision pipeline and OCR text extraction."

    exporter = PDFExporter()
    pdf_stream = exporter.generate_pdf(
        document_id=document_id,
        text=extracted_text,
        confidence=confidence,
        image_path=processed_path
    )

    filename = f"DocVision_{document_id}.pdf"
    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
