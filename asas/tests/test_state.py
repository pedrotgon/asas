from __future__ import annotations

from google.adk.sessions.database_session_service import DatabaseSessionService

from aido import session_service
from aido.state import (
    SESSION_STATUS_COMPLETED,
    SessionArtifacts,
    SessionState,
)


def test_session_state_roundtrip():
    artifacts = SessionArtifacts(
        video_path="E:/video.mp4",
        transcribed_text="hello",
        structured_data={"titulo": "Demo"},
        refined_structured_data={"titulo": "Demo"},
        json_string='{"titulo": "Demo"}',
        generated_docx_path="E:/manual.docx",
    )
    state = SessionState(
        session_id="abc",
        status=SESSION_STATUS_COMPLETED,
        artifacts=artifacts,
    )

    tool_state = state.to_tool_state()
    restored = SessionState.from_tool_state(tool_state)

    assert restored.session_id == "abc"
    assert restored.status == SESSION_STATUS_COMPLETED
    assert restored.artifacts.generated_docx_path == "E:/manual.docx"


def test_session_service_is_database_service():
    assert isinstance(session_service, DatabaseSessionService)
