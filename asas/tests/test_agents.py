from __future__ import annotations

from google.adk.agents import Agent, LlmAgent, SequentialAgent

from aido.agent import root_agent
from aido.config import paths
from aido.agents.concierge import concierge_tool
from aido.agents.create import create_tool
from aido.agents.create.pipeline import create_pipeline
from aido.agents.create.pipeline.subagents.json_converter.agent import json_converter_agent
from aido.agents.create.pipeline.subagents.mastering.agent import mastering_agent
from aido.agents.create.pipeline.subagents.structuring.agent import structuring_agent
from aido.agents.create.pipeline.subagents.transcription.agent import transcription_agent
from aido.agents.create.pipeline.subagents.writer.agent import writer_agent
from aido.agents.create.pipeline.subagents.session_recorder.agent import session_recorder_agent
from aido.agents.update import update_tool
from aido.agents.update.pipeline import update_pipeline
from aido.agents.update.pipeline.subagents.context_reader.agent import context_reader_agent
from aido.agents.update.pipeline.subagents.diff_planner.agent import diff_planner_agent
from aido.agents.update.pipeline.subagents.json_converter.agent import update_json_converter_agent
from aido.agents.update.pipeline.subagents.transcription.agent import update_transcription_agent
from aido.agents.update.pipeline.subagents.updater.agent import updater_agent
from aido.agents.update.pipeline.subagents.writer.agent import update_writer_agent
from aido.agents.update.pipeline.subagents.session_recorder.agent import (
    update_session_recorder_agent,
)


def test_root_agent_registers_tools():
    assert isinstance(root_agent, Agent)
    tool_names = {tool.name if isinstance(tool, Agent) else getattr(tool, "__name__", "")
                  for tool in root_agent.tools}
    assert concierge_tool in root_agent.tools
    assert create_tool in root_agent.tools
    assert update_tool in root_agent.tools
    assert "set_update_context" in tool_names


def test_create_pipeline_structure():
    assert isinstance(create_pipeline, SequentialAgent)
    expected = [
        transcription_agent,
        structuring_agent,
        mastering_agent,
        json_converter_agent,
        writer_agent,
        session_recorder_agent,
    ]
    assert create_pipeline.sub_agents == expected


def test_update_pipeline_structure():
    assert isinstance(update_pipeline, SequentialAgent)
    expected = [
        update_transcription_agent,
        context_reader_agent,
        diff_planner_agent,
        updater_agent,
        update_json_converter_agent,
        update_writer_agent,
        update_session_recorder_agent,
    ]
    assert update_pipeline.sub_agents == expected


def test_structuring_agent_is_configured():
    assert isinstance(structuring_agent, Agent)
    assert structuring_agent.output_key == "structured_data"
    assert "json" in structuring_agent.instruction.lower()


def test_mastering_agent_is_llm_agent():
    assert isinstance(mastering_agent, LlmAgent)
    assert mastering_agent.output_key == "refined_structured_data"


def test_json_converter_has_tool():
    assert json_converter_agent.output_key == "json_string"
    assert json_converter_agent.tools[0].__name__ == "convert_to_json_string"


def test_paths_defaults_within_project():
    assert paths.base_dir.joinpath("aido").exists()
    assert paths.input_dir.is_dir()
    assert paths.transcription_dir.is_dir()
    assert paths.docx_dir.is_dir()
    assert paths.templates_dir.is_dir()
    assert paths.template_file.exists()
    assert paths.base_storage_dir.is_dir()
    assert paths.database_dir.is_dir()
    assert paths.migrations_dir.is_dir()
    assert paths.logs_dir.is_dir()
    assert paths.database_url.startswith("sqlite:///")
