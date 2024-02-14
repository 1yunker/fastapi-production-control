from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.example')

    app_title: str = 'Default_title'
    echo: bool = True

    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'

    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    database_dsn: PostgresDsn | None = None

    project_host: str = '127.0.0.1'
    project_port: int = 8000


app_settings = AppSettings()
