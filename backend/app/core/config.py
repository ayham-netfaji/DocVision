from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "DocVision"
    api_v1_prefix: str = "/api/v1"
    upload_dir: Path = Path("uploads")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set[str] = {"jpg", "jpeg", "png", "webp"}

    model_config = {"env_prefix": "DOCVISION_"}


settings = Settings()
settings.upload_dir.mkdir(exist_ok=True)
