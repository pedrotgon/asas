from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator


SESSION_STATUS_CREATED = "created"
SESSION_STATUS_IN_PROGRESS = "in_progress"
SESSION_STATUS_COMPLETED = "completed"
SESSION_STATUS_FAILED = "failed"


class SessionArtifacts(BaseModel):
    """Artifacts produced throughout os pipelines de criacao/atualizacao."""

    video_path: Optional[str] = Field(default=None)
    transcribed_text: Optional[str] = Field(default=None)
    structured_data: Optional[Dict[str, Any]] = Field(default=None)
    refined_structured_data: Optional[Dict[str, Any]] = Field(default=None)
    json_string: Optional[str] = Field(default=None)
    generated_docx_path: Optional[str] = Field(default=None)
    previous_manual_path: Optional[str] = Field(default=None)
    previous_manual_text: Optional[str] = Field(default=None)
    update_plan: Optional[Dict[str, Any]] = Field(default=None)
    update_request: Optional[str] = Field(default=None)


class SessionState(BaseModel):
    """Canonical representation of the pipeline state for persistence."""

    session_id: Optional[str] = Field(default=None)
    status: str = Field(default=SESSION_STATUS_CREATED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = Field(default=None)
    artifacts: SessionArtifacts = Field(default_factory=SessionArtifacts)

    @field_validator("status")
    def validate_status(cls, value: str) -> str:
        allowed = {
            SESSION_STATUS_CREATED,
            SESSION_STATUS_IN_PROGRESS,
            SESSION_STATUS_COMPLETED,
            SESSION_STATUS_FAILED,
        }
        if value not in allowed:
            raise ValueError(f"Invalid session status '{value}'")
        return value

    def to_tool_state(self) -> Dict[str, Any]:
        """Serialise the Pydantic object back to a flat dict for tool_context."""

        data = {
            "session_id": self.session_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "error": self.error,
            "video_path": self.artifacts.video_path,
            "transcribed_text": self.artifacts.transcribed_text,
            "structured_data": self.artifacts.structured_data,
            "refined_structured_data": self.artifacts.refined_structured_data,
            "json_string": self.artifacts.json_string,
            "generated_docx_path": self.artifacts.generated_docx_path,
            "previous_manual_path": self.artifacts.previous_manual_path,
            "previous_manual_text": self.artifacts.previous_manual_text,
            "update_plan": self.artifacts.update_plan,
            "update_request": self.artifacts.update_request,
        }
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_tool_state(cls, state: Dict[str, Any]) -> "SessionState":
        """Builds a SessionState object from the ADK tool_context.state mapping."""

        structured_data = _coerce_dict(state.get("structured_data"))
        refined_data = _coerce_dict(state.get("refined_structured_data"))
        update_plan = _coerce_dict(state.get("update_plan"))

        return cls(
            session_id=state.get("session_id"),
            status=state.get("status", SESSION_STATUS_CREATED),
            created_at=_parse_datetime(state.get("created_at")),
            updated_at=_parse_datetime(state.get("updated_at")),
            error=state.get("error"),
            artifacts=SessionArtifacts(
                video_path=state.get("video_path"),
                transcribed_text=state.get("transcribed_text"),
                structured_data=structured_data,
                refined_structured_data=refined_data,
                json_string=state.get("json_string"),
                generated_docx_path=state.get("generated_docx_path"),
                previous_manual_path=state.get("previous_manual_path"),
                previous_manual_text=state.get("previous_manual_text"),
                update_plan=update_plan,
                update_request=state.get("update_request"),
            ),
        )

    def mark_in_progress(self) -> None:
        self.status = SESSION_STATUS_IN_PROGRESS
        self.updated_at = datetime.now(timezone.utc)

    def mark_completed(self) -> None:
        self.status = SESSION_STATUS_COMPLETED
        self.updated_at = datetime.now(timezone.utc)

    def mark_failed(self, message: str) -> None:
        self.status = SESSION_STATUS_FAILED
        self.error = message
        self.updated_at = datetime.now(timezone.utc)


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)
    return datetime.now(timezone.utc)


def _coerce_dict(value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return None


__all__ = [
    "SessionState",
    "SessionArtifacts",
    "SESSION_STATUS_CREATED",
    "SESSION_STATUS_IN_PROGRESS",
    "SESSION_STATUS_COMPLETED",
    "SESSION_STATUS_FAILED",
]
