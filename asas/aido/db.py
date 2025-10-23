from __future__ import annotations

import logging
from pathlib import Path

from google.adk.sessions.database_session_service import DatabaseSessionService

from .config import paths

logger = logging.getLogger(__name__)


def _ensure_sqlite_directory(database_url: str) -> None:
    """Ensure SQLite directories exist when using file based URLs."""

    if not database_url.startswith("sqlite:///"):
        return

    db_path = database_url.replace("sqlite:///", "", 1)
    sqlite_file = Path(db_path)
    sqlite_file.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_directory(paths.database_url)
session_service = DatabaseSessionService(paths.database_url)

logger.info("DatabaseSessionService initialised at %s", paths.database_url)


__all__ = ["session_service"]
