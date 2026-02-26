from pydantic_settings import BaseSettings, SettingsConfigDict

# fallback name and version if .env is not available

class Settings(BaseSettings):
    app_name: str = "eservice-workflow-api"
    app_version: str = "0.0.0"
    database_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()