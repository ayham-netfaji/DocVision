from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter()

class AITextRequest(BaseModel):
    text: str

class AITextResponse(BaseModel):
    result: str

@router.post("/summarize", response_model=AITextResponse)
async def summarize_text(request: AITextRequest):
    try:
        result = await ai_service.summarize_text(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/classify", response_model=AITextResponse)
async def classify_document(request: AITextRequest):
    try:
        result = await ai_service.classify_document(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
