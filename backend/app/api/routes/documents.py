import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import crud
from app.db.session import get_db
from app.schemas.document import DocumentScanResponse, ProcessingStagePreview
from app.utils.file_utils import validate_image_file

router = APIRouter()

@router.post("/scan", response_model=DocumentScanResponse)
async def scan_document(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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
            detail=f"Failed to process and store image: {e!s}"
        ) from e

    # 4. Computer Vision Preprocessing (Phase 5)
    import cv2

    from app.services.document_processor import DocumentProcessor
    from app.services.edge_detector import EdgeDetector
    from app.services.perspective import PerspectiveTransformer

    processor = DocumentProcessor()
    pipeline_res = processor.preprocess_pipeline(saved_path)

    # 5. Document Boundary Detection (Phase 6)
    edge_detector = EdgeDetector()
    edges = edge_detector.detect_edges(pipeline_res["blurred"])
    corners, _detected = edge_detector.find_document_contour(edges, pipeline_res["resized"].shape)

    # Save Stage 1: Grayscale
    gray_filename = f"{doc_id}_stage1_gray.png"
    cv2.imwrite(str(settings.upload_dir / gray_filename), pipeline_res["grayscale"])

    # Save Stage 2: Canny Edges
    edge_filename = f"{doc_id}_stage2_edges.png"
    cv2.imwrite(str(settings.upload_dir / edge_filename), edges)

    # Save Stage 3: Contour Quad Outline
    contour_preview = pipeline_res["resized"].copy()
    pts = corners.astype(int).reshape((-1, 1, 2))
    cv2.polylines(contour_preview, [pts], isClosed=True, color=(0, 255, 0), thickness=3)
    contour_filename = f"{doc_id}_stage3_contour.png"
    cv2.imwrite(str(settings.upload_dir / contour_filename), contour_preview)

    # 6. Perspective Correction / Homography Warp (Phase 7)
    transformer = PerspectiveTransformer()
    original_img = processor.load_image(saved_path)
    warped_doc = transformer.four_point_transform(
        original_img,
        corners,
        scale_ratio=pipeline_res["ratio"]
    )
    warped_filename = f"{doc_id}_stage4_warped.png"
    cv2.imwrite(str(settings.upload_dir / warped_filename), warped_doc)

    # 7. Image Enhancement (Phase 8)
    from app.services.image_enhancer import ImageEnhancer
    from app.services.ocr_service import OCRService

    enhancer = ImageEnhancer()
    enhanced_doc = enhancer.enhance(warped_doc, mode="scan_bw")

    processed_filename = f"{doc_id}_processed.png"
    processed_path = settings.upload_dir / processed_filename
    cv2.imwrite(str(processed_path), enhanced_doc)

    # 8. Optical Character Recognition (Phase 9)
    ocr_service = OCRService()
    ocr_result = ocr_service.extract_text(enhanced_doc)

    extracted_text = ocr_result.get("text", "")
    confidence = ocr_result.get("confidence", 95.0)
    word_count = ocr_result.get("word_count", 0)
    char_count = ocr_result.get("character_count", 0)

    if not extracted_text:
        extracted_text = "[No text detected in document image]"
        confidence = 0.0

    # 9. Persistent Database Storage (Phase 12)
    crud.create_document_record(
        db=db,
        doc_id=doc_id,
        filename=image.filename or filename,
        original_path=f"/uploads/{filename}",
        processed_path=f"/uploads/{processed_filename}",
        text=extracted_text,
        confidence=confidence,
        word_count=word_count,
        char_count=char_count
    )

    stages = [
        ProcessingStagePreview(
            id="1",
            name="Grayscale & Normalization",
            description="Normalized single channel representation",
            image_url=f"/uploads/{gray_filename}"
        ),
        ProcessingStagePreview(
            id="2",
            name="Canny Edge Detection",
            description="High-intensity gradients and edge maps",
            image_url=f"/uploads/{edge_filename}"
        ),
        ProcessingStagePreview(
            id="3",
            name="4-Point Boundary Detection",
            description="Convex polygon isolation of document boundaries",
            image_url=f"/uploads/{contour_filename}"
        ),
        ProcessingStagePreview(
            id="4",
            name="Perspective Rectification",
            description="Homography transformation flattening document top-down",
            image_url=f"/uploads/{warped_filename}"
        ),
        ProcessingStagePreview(
            id="5",
            name="Enhanced B&W Scan",
            description="CLAHE shadow removal & adaptive thresholding for OCR",
            image_url=f"/uploads/{processed_filename}"
        ),
    ]

    return DocumentScanResponse(
        document_id=doc_id,
        status="completed",
        original_image_url=f"/uploads/{filename}",
        processed_image_url=f"/uploads/{processed_filename}",
        text=extracted_text,
        confidence=confidence,
        word_count=word_count,
        character_count=char_count,
        stages=stages
    )

@router.get("")
async def list_documents(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """
    Returns list of all saved documents and their OCR summaries.
    """
    docs = crud.get_all_documents(db, limit=limit, offset=offset)
    return [
        {
            "document_id": d.id,
            "filename": d.filename,
            "status": d.status,
            "original_image_url": d.original_image_path,
            "processed_image_url": d.processed_image_path,
            "text": d.ocr_result.text if d.ocr_result else "",
            "confidence": d.ocr_result.confidence if d.ocr_result else 0.0,
            "word_count": d.ocr_result.word_count if d.ocr_result else 0,
            "character_count": d.ocr_result.character_count if d.ocr_result else 0,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in docs
    ]

@router.get("/{document_id}")
async def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = crud.get_document_by_id(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "original_image_url": doc.original_image_path,
        "processed_image_url": doc.processed_image_path,
        "text": doc.ocr_result.text if doc.ocr_result else "",
        "confidence": doc.ocr_result.confidence if doc.ocr_result else 0.0,
        "word_count": doc.ocr_result.word_count if doc.ocr_result else 0,
        "character_count": doc.ocr_result.character_count if doc.ocr_result else 0,
        "created_at": doc.created_at.isoformat() if doc.created_at else None
    }

@router.delete("/{document_id}")
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    success = crud.delete_document_by_id(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully", "document_id": document_id}
