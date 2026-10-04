from pydantic import BaseModel, Field
from typing import Optional, List


class OCRBoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int
    text: str
    confidence: float


class OCRResponse(BaseModel):
    raw_text: str
    cleaned_text: str
    confidence: float = Field(ge=0.0, le=100.0)
    word_count: int
    character_count: int
    boxes: Optional[List[OCRBoundingBox]] = None
