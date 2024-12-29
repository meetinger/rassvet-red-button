from pydantic_settings import BaseSettings, SettingsConfigDict

from project_root import PROJECT_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / '.env', extra='ignore')

    BOT_TOKEN: str

    # DB_USER: str
    # DB_PASSWORD: str
    # DB_HOST: str
    # DB_PORT: str
    # DB_NAME: str

    @property
    def db_url(self):
        # return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return f'sqlite+aiosqlite:///{PROJECT_ROOT}/database.sqlite3'

settings = Settings()
