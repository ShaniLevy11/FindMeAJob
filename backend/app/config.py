from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "findmeajob"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
