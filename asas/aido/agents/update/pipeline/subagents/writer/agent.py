from google.adk.agents import Agent

from aido.agents.create.pipeline.subagents.writer.tools.write_docx import write_docx


update_writer_agent = Agent(
    name="UpdateWriterAgent",
    model="gemini-2.5-flash",
    description="Gera a versao atualizada do manual em formato .docx.",
    tools=[write_docx],
    instruction="""
Use a string JSON atualizada salva em `{{json_string}}` como entrada para a ferramenta `write_docx`.
Nao informe argumentos adicionais; o sistema ja configura template e pasta de saida.

Ao final, devolva apenas o `output_path` retornado pela ferramenta.
""".strip(),
    output_key="generated_docx_path",
)


__all__ = ["update_writer_agent"]
