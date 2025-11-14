# from dotenv import load_dotenv
# load_dotenv()
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    AZURE_SQL_SERVER: str
    AZURE_SQL_DATABASE: str
    ODBC_DRIVER: str = "ODBC Driver 18 for SQL Server"   # <-- Add this default

    class Config:
        env_file = ".env"
        extra = "ignore"


db_settings = DatabaseSettings()

