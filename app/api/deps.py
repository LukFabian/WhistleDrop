from collections.abc import Generator
from sqlmodel import Session
from app.core.config import settings
from database.manager import DatabaseManager
from fastapi import Depends
from typing import Annotated

db_manager = DatabaseManager(settings.WHISTLE_DB_URL, settings.JOURNALIST_DB_URL, settings.ALEMBIC_PATH)


def get_whistle_db() -> Generator[Session, None, None]:
    with db_manager.get_whistle_session() as session:
        yield session


def get_journalist_db() -> Generator[Session, None, None]:
    with db_manager.get_journalist_session() as session:
        yield session


WhistleSessionDep = Annotated[Session, Depends(get_whistle_db)]
JournalistSessionDep = Annotated[Session, Depends(get_journalist_db)]
