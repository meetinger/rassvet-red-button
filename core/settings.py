from pydantic_settings import BaseSettings, SettingsConfigDict

from project_root import PROJECT_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / '.env', extra='ignore')

    BOT_TOKEN: str | None = None

    @property
    def db_url(self):
        return f'sqlite+aiosqlite:///{PROJECT_ROOT}/database.sqlite3'

settings = Settings()
