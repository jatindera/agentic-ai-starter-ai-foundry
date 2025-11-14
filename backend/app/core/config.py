from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Agentic AI Starter - AI Foundry"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "*"]

    class Config:
        env_file = ".env"

settings = Settings()
