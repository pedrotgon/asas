from google.adk.agents import Agent

diff_planner_agent = Agent(
    name="DiffPlannerAgent",
    model="gemini-2.5-flash",
    description="Analisa o manual atual e o novo conteudo para propor um plano de atualizacao.",
    instruction="""
Voce recebe o texto transcrito atualizado (`{{transcribed_text}}`), o manual anterior (`{{previous_manual_text}}`)
e as instrucoes do usuario (`{{update_request}}`).

Produza um plano em JSON com as chaves:
- secoes_alvo: lista das secoes que precisam ser alteradas.
- alteracoes_recomendadas: lista com descricoes objetivas das modificacoes.
- novos_itens: lista opcional com conteudos que precisam ser adicionados.
- riscos: pontos de atencao ao aplicar as mudanças.

Retorne apenas o JSON. Nao gere comentarios fora do objeto.
""".strip(),
    output_key="update_plan",
)


__all__ = ["diff_planner_agent"]
