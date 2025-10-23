from __future__ import annotations

from google.adk.agents import SequentialAgent

from .subagents.transcription.agent import update_transcription_agent
from .subagents.context_reader.agent import context_reader_agent
from .subagents.diff_planner.agent import diff_planner_agent
from .subagents.updater.agent import updater_agent
from .subagents.json_converter.agent import update_json_converter_agent
from .subagents.writer.agent import update_writer_agent
from .subagents.session_recorder.agent import update_session_recorder_agent


update_pipeline = SequentialAgent(
    name="update_pipeline",
    description="Pipeline sequencial que atualiza manuais existentes com base em novo material.",
    sub_agents=[
        update_transcription_agent,
        context_reader_agent,
        diff_planner_agent,
        updater_agent,
        update_json_converter_agent,
        update_writer_agent,
        update_session_recorder_agent,
    ],
)


__all__ = ["update_pipeline"]
