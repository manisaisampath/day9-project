from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Day 9 Project"
    api_base_url: str = "https://example.com"
    api_key: str = "replace_with_your_api_key"
    request_timeout: float = 10.0
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
