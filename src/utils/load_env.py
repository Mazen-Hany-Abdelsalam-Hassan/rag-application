from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    VERSION:str
    APP_NAME:str 

    OPENAI_KEY:Optional[str] = "OLLAMA"
    OPENAI_URL:str

    TEMPREATURE:float
    MAX_OUTPUT_TOKEN:int
    MAX_INPUT_TOKEN:int

    LLM_BACKEND:str
    EMBEDDING_MODEL_BACKEND:str
    
    LLM_MODEL:str
    EMBEDDING_MODEL_NAME:str
    EMBEDDING_MODEL_DIM:int


    class Config:
        env_file = '.env'
def get_settings():
    return Settings()