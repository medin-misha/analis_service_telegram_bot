from pydantic_sttings import BaseSettings
from dotenv import load_dotenv

import os

load_dotenv()


class Settings(BaseSettings):
    token: str = os.environ.get("bot_token")


settings = Settings()
