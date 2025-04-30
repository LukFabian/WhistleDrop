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
    WHISTLE_DB_URL: str = ""
    JOURNALIST_DB_URL: str = ""
    ALEMBIC_PATH: pathlib.PosixPath = pathlib.Path(
        file_path.parent.parent.parent.joinpath("whistledrop_alembic", "whistledrop_alembic.ini")).resolve()
    PROJECT_NAME: str = "StockScrape"
    SECRET_KEY: str = ""


settings = Settings()  # type: ignore
