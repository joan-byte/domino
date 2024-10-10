import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carga las variables de entorno desde el archivo .env en el directorio raíz
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
