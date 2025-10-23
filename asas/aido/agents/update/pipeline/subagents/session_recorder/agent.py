from google.adk.agents import Agent

from aido.agents.create.pipeline.subagents.session_recorder.agent import (
    finalize_session,
)

update_session_recorder_agent = Agent(
    name="UpdateSessionRecorderAgent",
    model="gemini-2.5-flash",
    description="Consolida os artefatos de atualizacao garantindo consistencia do estado.",
    instruction=(
        "Chame a ferramenta `finalize_session` para validar o estado apos a atualizacao. "
        "Retorne apenas um JSON com os campos retornados pela ferramenta."
    ),
    tools=[finalize_session],
    output_key="state_summary",
)


__all__ = ["update_session_recorder_agent"]
