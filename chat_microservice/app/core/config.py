from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGO_URI: str
    DATABASE_NAME: str = "chat_db"
    SECRET_KEY: str = "12345689"
    ACCESS_TOKEN_EXPIRE_MINUTES: str = "300"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = "../.env"


settings = Settings()
