from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Optional ,List

class Settings(BaseSettings):
    VERSION:str
    APP_NAME:str 
    ALLOWED_FILE_TYPES:List[str]
    MAXIMUM_ALLOWED_SIZE:int ## 5MIB of data 


    OPENAI_KEY:Optional[str] = "OLLAMA"
    OPENAI_URL:str
    CHUNK_SIZE:int
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