from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str | None = None

    openai_api_key: str

    @property
    def database_url(self) -> str:
        password = self.db_password
        auth = f"{self.db_user}:{password}" if password else self.db_user

        return "postgresql://" f"{auth}@{self.db_host}:{self.db_port}/{self.db_name}"


_settings: Settings | None = None


def get_app_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = (
            Settings()
        )  # pyright: ignore[reportCallIssue]. We want pydantic settings to fail if req env vars are missing.
    return _settings


def reset_app_settings_cache() -> None:
    global _settings
    _settings = None
