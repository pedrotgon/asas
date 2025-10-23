from google.adk.agents import Agent

from aido.agents.create.pipeline.subagents.json_converter.tool.convert_to_json_string import (
    convert_to_json_string,
)


update_json_converter_agent = Agent(
    name="UpdateJsonToStringAgent",
    model="gemini-2.5-flash",
    description="Converte o manual atualizado em uma string JSON formatada.",
    tools=[convert_to_json_string],
    instruction="""
Receba o objeto revisado armazenado em `{{refined_structured_data}}`.
Garanta que ele seja entregue para a ferramenta `convert_to_json_string` como argumento `data`.
Retorne somente a string JSON devolvida pela ferramenta.
""".strip(),
    output_key="json_string",
)


__all__ = ["update_json_converter_agent"]
