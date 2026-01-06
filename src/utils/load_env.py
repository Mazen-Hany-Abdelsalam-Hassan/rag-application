from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Optional, List

class Settings(BaseSettings):
    VERSION: str
    APP_NAME: str

    ALLOWED_FILE_TYPES: List[str]
    MAXIMUM_ALLOWED_SIZE: int  # bytes (e.g. 5 * 1024 * 1024)

    MONGO_DB_CLIENT: str
    MONGO_DB_NAME: str

    OPENAI_URL: str
    OPENAI_KEY: Optional[str] = None

    CHUNK_SIZE: int
    TEMPERATURE: float
    MAX_OUTPUT_TOKEN: int
    MAX_INPUT_TOKEN: int

    LLM_BACKEND: str
    EMBEDDING_MODEL_BACKEND: str

    LLM_MODEL: str
    EMBEDDING_MODEL_NAME: str
    EMBEDDING_MODEL_DIM: int

    VECTOR_DATABASE_NAME: str
    QDRANT_DATABASE_URL: Optional[str] = None
    QDRANT_DATABASE_PATH: Optional[str] = None

    DISTANCE_METRICS: str
    TOPK: int

    @model_validator(mode="after")
    def check_one_is_set(self):
        if not self.QDRANT_DATABASE_URL and not self.QDRANT_DATABASE_PATH:
            raise ValueError(
                "You must set either QDRANT_DATABASE_URL or QDRANT_DATABASE_PATH"
            )
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_settings() -> Settings:
    return Settings()
