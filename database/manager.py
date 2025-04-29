import pathlib

import sqlalchemy
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import sessionmaker, Session
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext


class DatabaseManager:
    """
    Manages the SQLAlchemy database connection and ensures the database
    is at the latest Alembic migration version.
    """

    def __init__(self, whistle_db_url: str, journalist_db_url: str, alembic_config_path: str | pathlib.Path):
        """
        Initialize the DatabaseManager.

        :param whistle_db_url: Database connection string (SQLAlchemy format).
        :param alembic_config_path: Path to the Alembic configuration file.
        """
        self.whistle_db_url = whistle_db_url
        self.journalist_db_url = journalist_db_url
        self.alembic_config_path = alembic_config_path
        self.whistledrop_engine: None | sqlalchemy.Engine = None
        self.journalist_engine: None | sqlalchemy.Engine = None
        self.whistle_session = None

        # Initialize database engine and session factory
        self._initialize_engines()
        self._check_alembic_versions()

    def _initialize_engines(self):
        """
        Creates the SQLAlchemy engine and session factory.
        """
        try:
            self.whistledrop_engine = create_engine(self.whistle_db_url, echo=False)
            self.journalist_engine = create_engine(self.journalist_db_url, echo=False)
            self.whistle_session = sessionmaker(autocommit=False, autoflush=False, bind=self.whistledrop_engine)
            self.journalist_session = sessionmaker(autocommit=False, autoflush=False, bind=self.journalist_engine)
            print("[INFO] Database engine initialized successfully.")

        except Exception as e:
            raise Exception(f"[ERROR] Failed to initialize database engine: {e}")

    def _get_current_whistle_db_version(self):
        """
        Fetch the current version of the database using Alembic's migration context.
        """
        with self.whistledrop_engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()

    def _get_current_journalist_db_version(self):
        """
        Fetch the current version of the database using Alembic's migration context.
        """
        with self.journalist_engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()

    def _get_latest_alembic_version(self):
        """
        Fetch the latest Alembic version from the migrations directory.
        """
        try:
            alembic_cfg = Config(self.alembic_config_path)
            script_directory = ScriptDirectory.from_config(alembic_cfg)
            head_revision = script_directory.get_current_head()
            return head_revision
        except Exception as e:
            raise Exception(f"[ERROR] Failed to fetch latest Alembic version: {e}")

    def _check_alembic_versions(self):
        """
        Compare the current database version to the latest Alembic version.
        Raise an error if they do not match.
        """
        try:
            current_whistle_version = self._get_current_whistle_db_version()
            current_journalist_version = self._get_current_journalist_db_version()
            conn = self.whistledrop_engine.connect()
            context = MigrationContext.configure(conn)
            latest_version = context.get_current_revision()
            conn.close()

            if current_whistle_version != latest_version:
                raise Exception(
                    f"[ERROR] Database version mismatch! Current: {current_whistle_version}, Expected: {latest_version}.\n"
                    "Run `whistledrop_alembic upgrade head` to migrate the database to the latest version."
                )

            conn = self.journalist_engine.connect()
            context = MigrationContext.configure(conn)
            latest_version = context.get_current_revision()
            conn.close()

            if current_journalist_version != latest_version:
                raise Exception(
                    f"[ERROR] Database version mismatch! Current: {current_whistle_version}, Expected: {latest_version}.\n"
                    "Run `whistledrop_alembic upgrade head` to migrate the database to the latest version."
                )

            print(f"[INFO] Database is at the latest version: {latest_version}.")

        except Exception as e:
            raise Exception(f"[ERROR] Database version check failed: {e}")

    def get_connection(self) -> Connection:
        """
        Get a new SQLAlchemy session.

        :return: A SQLAlchemy session.
        """
        return self.whistledrop_engine.connect()

    def get_whistle_session(self) -> Session:
        return Session(bind=self.whistledrop_engine)

    def get_journalist_session(self) -> Session:
        return Session(bind=self.journalist_engine)

    def close(self):
        """
        Closes the SQLAlchemy engine.
        """
        if self.whistledrop_engine:
            self.whistledrop_engine.dispose()
            print("[INFO] Database connection closed.")
