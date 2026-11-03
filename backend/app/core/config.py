from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str = "unsafe-development-secret-change-me"
    database_url: str = "sqlite:///./languagehub.db"
    cors_origins: str = "http://localhost:3000,http://localhost:8081"
    access_token_minutes: int = 60
    gemini_api_key: str = ""
    gemini_primary_model: str = "gemini-2.5-flash"
    gemini_fallback_model: str = "gemini-2.0-flash"
    ai_timeout_seconds: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.app_env.lower() == "production":
            if self.secret_key == "unsafe-development-secret-change-me" or len(self.secret_key) < 32:
                raise ValueError("Production SECRET_KEY must be a unique random value of at least 32 characters.")
        return self

    @property
    def allowed_origins(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

settings = Settings()
