from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn

class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    PINECONE_API_KEY: SecretStr
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str

    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

settings = Settings()