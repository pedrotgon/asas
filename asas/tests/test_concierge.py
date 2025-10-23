from __future__ import annotations

from types import SimpleNamespace

from aido.agents.concierge.tools.inspect_state import inspect_current_state


def make_context(initial_state: dict) -> SimpleNamespace:
    return SimpleNamespace(state=dict(initial_state), session_id="test-session")


def test_inspect_current_state_recommends_create_when_only_transcription():
    context = make_context(
        {
            "video_path": "E:/AI/Aido/data/entrada/demo.mp4",
            "transcribed_text": "conteudo",
        }
    )

    report = inspect_current_state(context)

    assert report["transcription_status"] == "in_state"
    assert report["recommended_action"] == "create_manual"


def test_inspect_current_state_detects_manual_ready(tmp_path):
    manual_path = tmp_path / "manual.docx"
    manual_path.write_text("dummy")

    context = make_context(
        {
            "video_path": str(tmp_path / "video.mp4"),
            "generated_docx_path": str(manual_path),
        }
    )

    report = inspect_current_state(context)

    assert report["manual_status"] == "ready"
    assert report["recommended_action"] == "manual_ready"
