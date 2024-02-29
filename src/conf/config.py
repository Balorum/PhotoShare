import cloudinary
from pydantic_settings import BaseSettings


def cloud_init():
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )


class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://user:password@localhost:5432/postgres"
    )
    secret_key: str = "secretkey"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "secretPassword"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = "secretPassword"
    cloudinary_name: str = "dmbcwijhm"
    cloudinary_api_key: int = 923533367683279
    cloudinary_api_secret: str = "Nhy698enrsQgiEnzFwuJl_mIddc"

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
