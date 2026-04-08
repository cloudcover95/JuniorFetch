from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    storage_path: Path = Path.home() / ".juniorfetch" / "palace"
    etch_threshold: float = 0.50
    embedding_dim: int = 512

    class Config:
        env_prefix = "JUNIORFETCH_"

settings = Settings()