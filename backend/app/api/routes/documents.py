import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas.document import DocumentScanResponse
from app.utils.file_utils import validate_image_file
from app.core.config import settings

router = APIRouter()

@router.post("/scan", response_model=DocumentScanResponse)
async def scan_document(
    image: UploadFile = File(...)
):
    """
    Accepts an uploaded image file, validates format and size,
    saves temporarily, and returns an initial scan stub response
    ready for OpenCV and OCR processing pipeline stages.
    """
    # 1. Validation
    ext = validate_image_file(image)
    
    # 2. Unique document identifier
    doc_id = uuid.uuid4().hex[:12]
    filename = f"{doc_id}.{ext}"
    saved_path = settings.upload_dir / filename
    
    # 3. Save file streaming with size limit checking
    total_size = 0
    try:
        with open(saved_path, "wb") as buffer:
            while chunk := await image.read(1024 * 1024):  # 1MB chunks
                total_size += len(chunk)
                if total_size > settings.max_file_size:
                    buffer.close()
                    if saved_path.exists():
                        saved_path.unlink()
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds maximum allowed size of {settings.max_file_size // (1024*1024)}MB."
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        if saved_path.exists():
            saved_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process and store image: {str(e)}"
        )

    # 4. Computer Vision Preprocessing (Phase 5)
    from app.services.document_processor import DocumentProcessor
    import cv2

    processor = DocumentProcessor()
    pipeline_res = processor.preprocess_pipeline(saved_path)
    
    # Save the normalized preprocessed grayscale/blurred image
    processed_filename = f"{doc_id}_processed.png"
    processed_path = settings.upload_dir / processed_filename
    cv2.imwrite(str(processed_path), pipeline_res["grayscale"])

    # 5. Response with live preview paths
    return DocumentScanResponse(
        document_id=doc_id,
        status="completed",
        original_image_url=f"/uploads/{filename}",
        processed_image_url=f"/uploads/{processed_filename}",
        text="[DocVision CV Core Preprocessed] Image normalized, resized, and grayscale converted with OpenCV. Ready for Phase 6 (Boundary & Contour Detection).",
        confidence=98.8
    )

@router.get("/{document_id}")
async def get_document(document_id: str):
    return {
        "document_id": document_id,
        "status": "ready"
    }
