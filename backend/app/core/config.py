from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Portal da Obra API"
    environment: str = "dev"
    database_url: str = "postgresql+psycopg2://portal:portal@postgres:5432/portal_obra"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    scheduler_enabled: bool = True
    scheduler_interval_minutes: int = 15
    sharepoint_mode: str = "mock"
    sharepoint_site_url: str = ""
    sharepoint_library: str = ""
    sharepoint_username: str = ""
    sharepoint_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
