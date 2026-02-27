from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FDV Engineering Docs API"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/fdv"
    upload_dir: str = "./storage/uploads"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
