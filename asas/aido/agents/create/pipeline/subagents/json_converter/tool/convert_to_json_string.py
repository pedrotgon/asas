import json
from typing import Any


def convert_to_json_string(data: Any) -> str:
    try:
        if isinstance(data, str):
            cleaned = _prepare_json_text(data)
            data = json.loads(cleaned)
        elif hasattr(data, "model_dump"):
            data = data.model_dump()

        return json.dumps(data, ensure_ascii=False, indent=4)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"structured_data was not valid JSON: {exc}"
        ) from exc
    except TypeError as exc:
        raise ValueError(
            f"structured_data contains unsupported types: {exc}"
        ) from exc
    except Exception as exc:  # pragma: no cover - safeguard
        raise ValueError(f"unexpected error converting structured_data: {exc}") from exc


def _prepare_json_text(raw: str) -> str:
    text = raw.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    if not text.startswith("{") and "{" in text:
        start = text.find("{")
        end = text.rfind("}")
        if end > start:
            text = text[start : end + 1]

    return text
