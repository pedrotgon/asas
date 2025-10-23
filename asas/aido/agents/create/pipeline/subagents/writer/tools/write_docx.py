from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, Optional

from docxtpl import DocxTemplate
from google.adk.tools.tool_context import ToolContext

from aido.config import paths
from aido.state import SESSION_STATUS_COMPLETED, SESSION_STATUS_FAILED
from aido.agents.create.pipeline.subagents.json_converter.tool.convert_to_json_string import (
    _prepare_json_text,
)


def _ensure_within(base: Path, target: Path, label: str) -> Optional[str]:
    try:
        target.relative_to(base)
    except ValueError:
        return f"Security Error: {label} '{target}' is not inside '{base}'."
    return None


def _resolve_template_path(template_path: Optional[str]) -> Path:
    if template_path:
        return Path(template_path).expanduser().resolve()
    return paths.template_file


def _resolve_output_dir(output_dir: Optional[str]) -> Path:
    if output_dir:
        return Path(output_dir).expanduser().resolve()
    return paths.docx_dir


def _write_docx_sync(
    structured_data: str,
    template_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        template_path_abs = _resolve_template_path(template_path)
        output_dir_abs = _resolve_output_dir(output_dir)

        error = _ensure_within(paths.templates_dir, template_path_abs, "Template path")
        if error:
            return {"status": "error", "message": error}

        error = _ensure_within(paths.docx_dir.parent, output_dir_abs, "Output directory")
        if error:
            return {"status": "error", "message": error}

        if not template_path_abs.exists():
            return {"status": "error", "message": f"Template file not found at {template_path_abs}"}

        output_dir_abs.mkdir(parents=True, exist_ok=True)

        doc = DocxTemplate(str(template_path_abs))
        prepared_payload = _prepare_json_text(structured_data)
        context = json.loads(prepared_payload)
        doc.render(context)

        title = context.get("titulo") or context.get("title") or "Generated_Manual"
        safe_filename = "".join(char for char in title if char.isalnum() or char in (" ", "-")).rstrip()
        output_filename = safe_filename.replace(" ", "_") + ".docx"
        output_path = output_dir_abs / output_filename
        doc.save(str(output_path))

        return {"status": "success", "output_path": str(output_path)}

    except json.JSONDecodeError:
        return {"status": "error", "message": "Input data was not valid JSON."}
    except Exception as exc:  # pragma: no cover - defensive
        return {"status": "error", "message": f"An unexpected error occurred: {exc}"}


async def write_docx(
    structured_data: str,
    template_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    print("--- TOOL: Initializing .docx generation ---")

    result = await asyncio.to_thread(
        _write_docx_sync,
        structured_data,
        template_path,
        output_dir,
    )

    if result["status"] == "success":
        print(f"--- TOOL: Successfully generated document at {result['output_path']} ---")
        if tool_context is not None:
            tool_context.state["generated_docx_path"] = result["output_path"]
            tool_context.state["status"] = SESSION_STATUS_COMPLETED
    else:
        print(f"--- TOOL ERROR: {result['message']} ---")
        if tool_context is not None:
            tool_context.state["status"] = SESSION_STATUS_FAILED
            tool_context.state["error"] = result["message"]

    return result
