from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql+asyncpg://postgres:111111@localhost:5432/abc"
    CLD_NAME: str = 'photoshare'
    CLD_API_KEY: str = '123123123'
    CLD_API_SECRET: str = '222dcsds00'
    model_config = ConfigDict(extra='ignore', env_file=".env.example", env_file_encoding="utf-8")  # noqa


settings = Settings()
