from google.adk.agents import Agent

updater_agent = Agent(
    name="UpdaterAgent",
    model="gemini-2.5-flash",
    description="Aplica o plano de atualizacao ao manual existente, gerando JSON estruturado revisado.",
    instruction="""
Voce recebe:
- Transcricao atualizada (`{{transcribed_text}}`)
- Manual anterior (`{{previous_manual_text}}`)
- Plano de alteracoes (`{{update_plan}}`)

Produza um JSON seguindo o mesmo formato do `StructuredManual`, atualizando apenas o que for necessario.
Mantenha campos nao mencionados no plano. Garanta consistencia e formate listas em Markdown.
Retorne somente o JSON.
""".strip(),
    output_key="refined_structured_data",
)


__all__ = ["updater_agent"]
