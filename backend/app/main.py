from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.documents import router as documents_router
from app.api.routes.ocr import router as ocr_router
from app.api.routes.export import router as export_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Computer Vision Document Scanner and OCR Text Extraction API"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API Routers
    app.include_router(health_router, prefix=settings.api_v1_prefix, tags=["Health"])
    app.include_router(documents_router, prefix=f"{settings.api_v1_prefix}/documents", tags=["Documents"])
    app.include_router(ocr_router, prefix=f"{settings.api_v1_prefix}/ocr", tags=["OCR"])
    app.include_router(export_router, prefix=f"{settings.api_v1_prefix}/export", tags=["Export"])

    # Static file serving for uploads during dev
    app.mount("/uploads", StaticFiles(directory=str(settings.upload_dir)), name="uploads")

    return app


app = create_app()
