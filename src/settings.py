import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")

    POSTGRES_DB: str | None = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str | None = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SUPERUSER_EMAIL: EmailStr | None = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str | None = os.getenv("SUPERUSER_PASSWORD")


settings = Settings()
