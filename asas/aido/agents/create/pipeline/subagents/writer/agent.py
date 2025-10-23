from google.adk.agents import Agent

from .tools.write_docx import write_docx


writer_agent = Agent(
    name="WriterAgent",
    model="gemini-2.5-flash",
    description="Gera o manual final em formato .docx utilizando o template padrao.",
    tools=[write_docx],
    instruction="""
Use a string JSON salva em `{{json_string}}` como entrada para a ferramenta `write_docx`.
Ao chamar a ferramenta, passe `structured_data={{json_string}}`. Os demais argumentos sao
pre-configurados pelo sistema e nao precisam ser enviados.

Depois da execucao da ferramenta, responda somente com o valor da chave `output_path`
retornado pela ferramenta. Nao inclua nenhum outro texto.
""".strip(),
    output_key="generated_docx_path",
)


__all__ = ["writer_agent"]
