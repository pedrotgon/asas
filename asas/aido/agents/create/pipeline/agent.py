from __future__ import annotations

from google.adk.agents import SequentialAgent

from .subagents.transcription.agent import transcription_agent
from .subagents.structuring.agent import structuring_agent
from .subagents.mastering.agent import mastering_agent
from .subagents.json_converter.agent import json_converter_agent
from .subagents.writer.agent import writer_agent
from .subagents.session_recorder.agent import session_recorder_agent


create_pipeline = SequentialAgent(
    name="create_pipeline",
    description="Pipeline sequencial que transforma videos em manuais estruturados.",
    sub_agents=[
        transcription_agent,
        structuring_agent,
        mastering_agent,
        json_converter_agent,
        writer_agent,
        session_recorder_agent,
    ],
)


__all__ = ["create_pipeline"]
