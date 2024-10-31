import logging
import dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dotenv.load_dotenv()
    LAT: float
    LON: float
    UNITS: str
    API_KEY: str
    DB_URI: str


settings = Settings()

log = logging.getLogger('uvicorn.error')
