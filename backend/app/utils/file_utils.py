from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


def validate_image_file(file: UploadFile) -> str:
    """
    Validates uploaded file MIME type and extension.
    Returns cleaned file extension (e.g., 'jpg', 'png').
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing or invalid."
        )

    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: '{ext}'. Allowed extensions: {', '.join(settings.allowed_extensions)}"
        )

    valid_content_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type and file.content_type.lower() not in valid_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid MIME content type: '{file.content_type}'. Must be JPEG, PNG, or WEBP."
        )

    return ext
