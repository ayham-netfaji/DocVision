from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def ocr_engine_status():
    """
    Returns OCR engine status and readiness.
    """
    return {
        "engine": "Tesseract OCR",
        "status": "ready",
        "phase": "Phase 3 Scaffolded"
    }
