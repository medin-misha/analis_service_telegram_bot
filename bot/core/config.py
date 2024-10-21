from pydantic_settings import BaseSettings
from dotenv import load_dotenv

import os

load_dotenv()


class Settings(BaseSettings):
    token: str
    server: str
    parse_mode: str = "HTML"

    class Config:
        env_file = ".env"


settings = Settings()
