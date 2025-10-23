from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from aido.state import (
    SESSION_STATUS_COMPLETED,
    SESSION_STATUS_FAILED,
    SESSION_STATUS_IN_PROGRESS,
    SessionState,
)


def finalize_session(tool_context: ToolContext) -> Dict[str, str]:
    """Validate the session state and persist final metadata."""

    session_state = SessionState.from_tool_state(tool_context.state)

    if getattr(tool_context, "session_id", None):
        session_state.session_id = tool_context.session_id

    generated_doc = session_state.artifacts.generated_docx_path
    error_message = tool_context.state.get("error")

    if error_message:
        session_state.mark_failed(str(error_message))
    elif generated_doc:
        session_state.mark_completed()
    else:
        session_state.mark_in_progress()

    session_state.updated_at = datetime.now(timezone.utc)
    tool_context.state.update(session_state.to_tool_state())

    summary = {
        "status": session_state.status,
        "generated_docx_path": generated_doc or "",
        "session_id": session_state.session_id or "",
    }

    return summary


session_recorder_agent = Agent(
    name="SessionRecorderAgent",
    model="gemini-2.5-flash",
    description="Consolida os artefatos gerados e garante a consistencia do estado da sessao.",
    instruction=(
        "Chame a ferramenta `finalize_session` para validar e consolidar o estado. "
        "Retorne apenas um JSON com os campos retornados pela ferramenta."
    ),
    tools=[finalize_session],
    output_key="state_summary",
)


__all__ = ["session_recorder_agent", "finalize_session"]
