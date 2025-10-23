from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from google.adk.tools.tool_context import ToolContext


def load_manual(manual_path: str, tool_context: Optional[ToolContext] = None) -> str:
    """Load existing manual content (txt or json) so the pipeline can compare."""

    if not manual_path:
        raise ValueError("manual_path nao informado.")

    path_obj = Path(manual_path).expanduser().resolve()
    if not path_obj.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path_obj}")

    if path_obj.suffix.lower() == ".json":
        content = json.dumps(json.loads(path_obj.read_text(encoding="utf-8")), ensure_ascii=False, indent=2)
    else:
        content = path_obj.read_text(encoding="utf-8", errors="ignore")

    if tool_context is not None:
        tool_context.state["previous_manual_path"] = str(path_obj)
        tool_context.state["previous_manual_text"] = content

    return content
