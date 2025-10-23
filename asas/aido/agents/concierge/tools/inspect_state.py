from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from google.adk.tools.tool_context import ToolContext

from aido.config import paths
from aido.state import SessionState


def _file_exists(path_str: Optional[str]) -> bool:
    if not path_str:
        return False
    return Path(path_str).expanduser().resolve().exists()


def _transcription_cached(video_path: Optional[str]) -> Optional[str]:
    if not video_path:
        return None
    candidate = Path(video_path).expanduser().resolve()
    cache_path = paths.transcription_dir / f"{candidate.stem}_transcricao.txt"
    return str(cache_path) if cache_path.exists() else None


def inspect_current_state(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    if tool_context is None:
        raise ValueError("Tool context indisponível.")

    state_mapping: Dict[str, Any] = dict(tool_context.state)
    session_state = SessionState.from_tool_state(state_mapping)

    video_path = session_state.artifacts.video_path
    transcribed_text = session_state.artifacts.transcribed_text
    manual_path = session_state.artifacts.generated_docx_path
    previous_manual_path = session_state.artifacts.previous_manual_path

    cached_transcription_path = _transcription_cached(video_path)

    transcription_status = "missing"
    if transcribed_text:
        transcription_status = "in_state"
    elif cached_transcription_path:
        transcription_status = "cached"

    manual_status = "missing"
    if manual_path and _file_exists(manual_path):
        manual_status = "ready"

    previous_manual_status = "missing"
    if previous_manual_path and _file_exists(previous_manual_path):
        previous_manual_status = "ready"
    elif previous_manual_path:
        previous_manual_status = "not_found"

    recommended_action = "await_input"
    if manual_status == "ready":
        recommended_action = "manual_ready"
    elif transcription_status in {"in_state", "cached"} and previous_manual_status == "ready":
        recommended_action = "update_manual"
    elif transcription_status in {"in_state", "cached"}:
        recommended_action = "create_manual"
    else:
        recommended_action = "transcribe"

    report = {
        "video_path": video_path,
        "transcription_status": transcription_status,
        "transcription_cache_path": cached_transcription_path,
        "manual_status": manual_status,
        "manual_path": manual_path,
        "previous_manual_status": previous_manual_status,
        "previous_manual_path": previous_manual_path,
        "recommended_action": recommended_action,
    }

    # Persist derived info for próximos agentes.
    tool_context.state.update({k: v for k, v in report.items() if v is not None})

    return report


__all__ = ["inspect_current_state"]
