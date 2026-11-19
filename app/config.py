
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    BLUESKY_HANDLE: str = ""
    BLUESKY_PASSWORD: str = ""

    MASTODON_BASE_URL: str = ""
    MASTODON_ACCESS_TOKEN: str = ""
    DISCORD_WEBHOOK_URL: str = ""
    DEVTO_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    GITHUB_OWNER: str = ""
    GITHUB_REPO: str = ""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
