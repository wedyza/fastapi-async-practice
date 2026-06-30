
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_USE_SSL: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


class RedisSettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

class Settings(BaseSettings):
    LAUNCHED_IN_CONTAINER: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EMAIL_SETTINGS: EmailSettings = EmailSettings()  # pyright: ignore[reportCallIssue]
    REDIS_SETTINGS: RedisSettings = RedisSettings()
    TEMPLATES_DIR: str = "src.app.templates"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

settings = Settings()
