from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Iterable, Tuple, Union, Optional

from aido.config import paths
from aido.state import SESSION_STATUS_IN_PROGRESS
from google.adk.tools.tool_context import ToolContext

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover - optional dependency
    WhisperModel = None  # type: ignore[assignment]


TRANSCRIPTION_CACHE_DIR = paths.transcription_dir
ALLOWED_DIRECTORY = paths.input_dir


def _ensure_model() -> "WhisperModel":
    if WhisperModel is None:
        raise RuntimeError(
            "faster-whisper is not installed. Install it to enable transcription."
        )
    return WhisperModel("tiny", device="cpu", compute_type="int8")


def _run_transcription_sync(video_path: Union[str, Path]) -> Tuple[Iterable, object]:
    model = _ensure_model()
    segments, info = model.transcribe(str(video_path), beam_size=5)
    return segments, info


async def transcribe_video(
    video_path: str, tool_context: Optional[ToolContext] = None
) -> str:
    video_path_obj = Path(video_path).expanduser().resolve()
    print(f"--- TOOL: Requesting transcription for {video_path_obj} ---")

    try:
        video_path_obj.relative_to(ALLOWED_DIRECTORY)
    except ValueError:
        error_msg = (
            f"Security Error: Path '{video_path_obj}' is outside the allowed directory."
        )
        print(f"--- TOOL ERROR: {error_msg} ---")
        return f"Error: {error_msg}"

    if not video_path_obj.exists():
        error_msg = f"Video file not found at {video_path_obj}"
        print(f"--- TOOL ERROR: {error_msg} ---")
        return f"Error: {error_msg}"

    cache_filename = f"{video_path_obj.stem}_transcricao.txt"
    cache_file_path = TRANSCRIPTION_CACHE_DIR / cache_filename

    if cache_file_path.exists():
        print(f"--- TOOL: Cache hit! Reading transcription from {cache_file_path} ---")
        try:
            return cache_file_path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover - defensive
            print(
                f"--- TOOL WARNING: Could not read cache file. Retranscribing. Error: {exc} ---"
            )

    print("--- TOOL: No cache found. Initializing transcription with retry logic. ---")
    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        try:
            segments, info = await asyncio.to_thread(
                _run_transcription_sync, video_path_obj
            )
            language = getattr(info, "language", "unknown")
            probability = getattr(info, "language_probability", 0.0)
            print(
                f"--- TOOL: Detected language '{language}' with probability {probability:.2f} ---"
            )
            transcribed_text = "".join(segment.text for segment in segments).strip()

            print(f"--- TOOL: Transcription successful. Saving to cache at {cache_file_path} ---")
            cache_file_path.write_text(transcribed_text, encoding="utf-8")

            if tool_context is not None:
                tool_context.state["video_path"] = str(video_path_obj)
                tool_context.state["status"] = SESSION_STATUS_IN_PROGRESS
                if getattr(tool_context, "session_id", None):
                    tool_context.state["session_id"] = tool_context.session_id

            return transcribed_text

        except Exception as exc:
            print(f"--- TOOL WARNING: Attempt {attempt + 1} of {max_retries} failed. Error: {exc} ---")
            if attempt + 1 == max_retries:
                error_message = f"An unexpected error occurred after {max_retries} attempts: {exc}"
                print(f"--- TOOL ERROR: {error_message} ---")
                return f"Error: {error_message}"

            delay = base_delay * (2**attempt)
            print(f"--- TOOL: Retrying in {delay} seconds... ---")
            await asyncio.sleep(delay)
