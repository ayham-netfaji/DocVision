from datetime import UTC, datetime

from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    filename: str
    content_type: str
    size_bytes: int


class ProcessingStagePreview(BaseModel):
    id: str
    name: str
    description: str
    image_url: str


class DocumentScanResponse(BaseModel):
    document_id: str
    status: str = Field(default="completed", description="Status: completed, processing, failed")
    original_image_url: str
    processed_image_url: str | None = None
    text: str
    confidence: float
    word_count: int | None = 0
    character_count: int | None = 0
    stages: list[ProcessingStagePreview] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DocumentErrorResponse(BaseModel):
    detail: str
    error_code: str
