"""
Callbacks e guardrails inspirados no Tutorial 09.

As funcoes abaixo ainda sao conservadoras: registram algumas informacoes no estado
e retornam None para nao interferir no fluxo padrao. Elas servem como ponto unico
para enriquecer auditoria/seguranca sem espalhar logica pelos agentes.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from google.adk.agents.callback_context import CallbackContext


def _ensure_metrics(callback_context: CallbackContext) -> Dict[str, Any]:
    """Atualiza dicionario de metricas no estado do callback."""

    state = getattr(callback_context, "state", None)
    if state is None:
        state = callback_context.state = {}

    metrics = state.setdefault("metrics", {})
    return metrics


def before_agent_callback(callback_context: CallbackContext) -> Optional[Any]:
    metrics = _ensure_metrics(callback_context)
    metrics["agent_calls"] = metrics.get("agent_calls", 0) + 1
    return None


def after_agent_callback(callback_context: CallbackContext, content: Any) -> Optional[Any]:
    metrics = _ensure_metrics(callback_context)
    metrics["last_agent_response"] = str(content)
    return None


def before_tool_callback(callback_context: CallbackContext, tool_input: Dict[str, Any]) -> Optional[Any]:
    metrics = _ensure_metrics(callback_context)
    tool_name = getattr(callback_context, "tool_name", "unknown_tool")
    history = metrics.setdefault("tool_invocations", [])
    history.append(tool_name)
    return None


def after_tool_callback(
    callback_context: CallbackContext, tool_input: Dict[str, Any], tool_output: Any
) -> Optional[Any]:
    metrics = _ensure_metrics(callback_context)
    metrics["last_tool_output"] = tool_output
    return None


DEFAULT_CALLBACKS = {
    "before_agent": before_agent_callback,
    "after_agent": after_agent_callback,
    "before_tool": before_tool_callback,
    "after_tool": after_tool_callback,
}


__all__ = [
    "before_agent_callback",
    "after_agent_callback",
    "before_tool_callback",
    "after_tool_callback",
    "DEFAULT_CALLBACKS",
]
