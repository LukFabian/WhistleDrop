import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

file_path = pathlib.Path(__file__).resolve()


class Settings(BaseSettings):
    # Use top level .env file
    model_config = SettingsConfigDict(
        env_file=file_path.parent.parent.parent.joinpath(".env"),
        env_ignore_empty=True,
        extra="ignore",
    )
    DB_PORT: int = 0
    DB_HOST: str = ""
    DB_URL: str = ""
    ALEMBIC_PATH: pathlib.PosixPath = pathlib.Path(file_path.parent.parent.parent.joinpath("alembic", "alembic.ini")).resolve()
    PROJECT_NAME: str = "StockScrape"


settings = Settings()  # type: ignore
