"""
Configuration helpers for the Aido agents.

The production tutorials (see tutorial04 and tutorial06) keep all file-system
concerns outside of the agent prompts. This module follows the same idea:
paths can be customised with environment variables while keeping safe
defaults relative to the repository root.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ENV_DATA_ROOT = "AIDO_DATA_ROOT"
ENV_INPUT_DIR = "AIDO_INPUT_DIR"
ENV_TRANSCRIPTION_DIR = "AIDO_TRANSCRIPTION_DIR"
ENV_DOCX_DIR = "AIDO_DOCX_DIR"
ENV_TEMPLATES_DIR = "AIDO_TEMPLATES_DIR"
ENV_TEMPLATE_PATH = "AIDO_TEMPLATE_PATH"
ENV_BASE_STORAGE = "AIDO_BASE_STORAGE"
ENV_DATABASE_URL = "AIDO_DATABASE_URL"


@dataclass(frozen=True)
class AidoPaths:
    """Container with resolved paths used across the pipeline."""

    base_dir: Path
    data_root: Path
    input_dir: Path
    transcription_dir: Path
    docx_dir: Path
    templates_dir: Path
    template_file: Path
    base_storage_dir: Path
    database_dir: Path
    migrations_dir: Path
    logs_dir: Path
    database_url: str


def _resolve_path(env_name: str, default: Path) -> Path:
    """Resolve a path from environment or fall back to the provided default."""

    raw_value = os.environ.get(env_name)
    if not raw_value:
        return default
    return Path(raw_value).expanduser().resolve()


def load_paths() -> AidoPaths:
    """Materialise the directory layout using environment overrides when set."""

    project_root = Path(__file__).resolve().parents[1]

    base_storage_dir = _resolve_path(
        ENV_BASE_STORAGE, project_root / "data" / "base"
    ).resolve()

    data_root = _resolve_path(ENV_DATA_ROOT, project_root / "data").resolve()
    input_dir = _resolve_path(ENV_INPUT_DIR, data_root / "entrada").resolve()
    transcription_dir = _resolve_path(
        ENV_TRANSCRIPTION_DIR, data_root / "saida" / "txt"
    ).resolve()
    docx_dir = _resolve_path(ENV_DOCX_DIR, data_root / "saida" / "docx").resolve()
    templates_dir = _resolve_path(ENV_TEMPLATES_DIR, project_root / "templates").resolve()
    template_file = _resolve_path(
        ENV_TEMPLATE_PATH, templates_dir / "Padronizacao_Manuais.docx"
    ).resolve()

    database_dir = (base_storage_dir / "sqlite").resolve()
    migrations_dir = (base_storage_dir / "migrations").resolve()
    logs_dir = (base_storage_dir / "logs").resolve()

    # Ensure writable directories exist (mirrors patterns from tutorial04).
    base_storage_dir.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(parents=True, exist_ok=True)
    migrations_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    transcription_dir.mkdir(parents=True, exist_ok=True)
    docx_dir.mkdir(parents=True, exist_ok=True)

    default_database_path = database_dir / "aido_data.db"
    default_database_url = f"sqlite:///{default_database_path.as_posix()}"
    database_url = os.environ.get(ENV_DATABASE_URL, default_database_url)

    return AidoPaths(
        base_dir=project_root,
        data_root=data_root,
        input_dir=input_dir,
        transcription_dir=transcription_dir,
        docx_dir=docx_dir,
        templates_dir=templates_dir,
        template_file=template_file,
        base_storage_dir=base_storage_dir,
        database_dir=database_dir,
        migrations_dir=migrations_dir,
        logs_dir=logs_dir,
        database_url=database_url,
    )


paths = load_paths()


__all__ = [
    "AidoPaths",
    "ENV_DATA_ROOT",
    "ENV_INPUT_DIR",
    "ENV_TRANSCRIPTION_DIR",
    "ENV_DOCX_DIR",
    "ENV_TEMPLATES_DIR",
    "ENV_TEMPLATE_PATH",
    "ENV_BASE_STORAGE",
    "ENV_DATABASE_URL",
    "load_paths",
    "paths",
]
