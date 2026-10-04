from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class DocumentBase(BaseModel):
    filename: str
    content_type: str
    size_bytes: int


class DocumentScanResponse(BaseModel):
    document_id: str
    status: str = Field(default="completed", description="Status: completed, processing, failed")
    original_image_url: str
    processed_image_url: Optional[str] = None
    text: str
    confidence: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentErrorResponse(BaseModel):
    detail: str
    error_code: str
