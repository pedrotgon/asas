from __future__ import annotations

from typing import Optional

from google.adk.tools.tool_context import ToolContext


def set_update_context(
    manual_path: str,
    update_request: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> str:
    if tool_context is None:
        raise ValueError("Tool context indisponivel.")

    if manual_path:
        tool_context.state["previous_manual_path"] = manual_path

    if update_request:
        tool_context.state["update_request"] = update_request

    return "Contexto de atualizacao registrado."


__all__ = ["set_update_context"]
