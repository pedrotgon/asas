from google.adk.agents import Agent

from .tools.load_manual import load_manual


context_reader_agent = Agent(
    name="ContextReaderAgent",
    model="gemini-2.5-flash",
    description="Carrega o manual/JSON existente para comparar com o novo material.",
    tools=[load_manual],
    instruction="""
Verifique se `previous_manual_path` esta definido no estado atual.
Chame a ferramenta `load_manual`, passando esse caminho como argumento `manual_path`.
Caso o caminho nao esteja presente, solicite ao usuario que informe um arquivo `.txt` ou `.json`.
Depois da leitura, retorne somente o texto carregado. Não inclua comentarios extras.
""".strip(),
    output_key="previous_manual_text",
)


__all__ = ["context_reader_agent"]
