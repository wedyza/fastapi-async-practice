from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    POSTGRES_HOST: str
    DATABASE_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def database_url_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.DATABASE_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # pyright: ignore[reportUnannotatedClassAttribute]

settings = DBSettings()  # pyright: ignore[reportCallIssue]
