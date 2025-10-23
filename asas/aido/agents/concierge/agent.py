from google.adk.agents import Agent

from .tools.inspect_state import inspect_current_state


concierge_agent = Agent(
    name="ConciergeAgent",
    model="gemini-2.5-flash",
    description=(
        "Analista que verifica se transcrição, manual e artefatos já existem antes de acionar pipelines."
    ),
    tools=[inspect_current_state],
    instruction=(
        "Revise o estado atual chamando a ferramenta `inspect_current_state`. "
        "Resuma o resultado em português, informando se a transcrição existe, se há manual anterior "
        "e qual é o próximo passo recomendado (criar manual, atualizar manual ou aguardar mais dados). "
        "Não invente dados; apenas use o retorno da ferramenta."
    ),
    output_key="concierge_report",
)


__all__ = ["concierge_agent"]
