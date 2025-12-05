from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import Optional
class Settings(BaseSettings):
    VERSION:str
    APP_NAME:str    
    class Config:
        env_file = '.env'
def get_settings():
    return Settings()