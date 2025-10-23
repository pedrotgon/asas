# Sprint Bônus — Agente de Atualização (Agent-as-a-Tool Update)

Este sprint bônus introduz um pipeline completo para atualização de manuais, reorganiza a estrutura de pastas segundo as melhores práticas do ADK e prepara o terreno para personalização baseada em memória de usuário.

---

## 1. Backlog da Sprint ✅
| ID | Sub-tarefa | Resultado |
| --- | --- | --- |
| SB-T01 | Reestruturar diretórios (agents/create, agents/update, shared). | [ ] |
| SB-T02 | Implementar AgentTool update_tool com SequentialAgent dedicado. | [ ] |
| SB-T03 | Adicionar subagentes do update (context reader, diff planner, updater etc.). | [ ] |
| SB-T04 | Integrar human-in-loop no root agent para coletar instruções de atualização. | [ ] |
| SB-T05 | Expandir SessionState (campos de atualização) e persistência. | [ ] |
| SB-T06 | Criar testes para novo pipeline/update e atualizar documentação. | [ ] |

---

## 2. Visão Geral da Solução 🚀
- Nova estrutura em ido/agents/ separa Agent-as-a-Tool por finalidade (create, update) com seus pipelines e subagentes.
- oot_agent decide quando usar criação ou atualização; para updates, executa um mini fluxo de perguntas antes de chamar o pipeline.
- update pipeline inclui leitura do manual anterior, geração de plano de mudança e reescrita parcial.
- SessionState guarda artefatos de atualização (caminho do doc anterior, plano de diffs, resultado final).

---

## 3. Novo Layout de Pastas
`
aido/
├── agent.py
├── config.py, db.py, state.py
├── agents/
│   ├── create/
│   │   ├── tool.py
│   │   └── pipeline/
│   │       ├── agent.py
│   │       └── subagents/
│   │           ├── transcription/
│   │           ├── structuring/
│   │           ├── mastering/
│   │           ├── json_converter/
│   │           ├── writer/
│   │           └── session_recorder/
│   └── update/
│       ├── tool.py
│       └── pipeline/
│           ├── agent.py
│           └── subagents/
│               ├── transcription/
│               ├── context_reader/
│               ├── diff_planner/
│               ├── updater/
│               ├── json_converter/
│               ├── writer/
│               └── session_recorder/
├── shared/
│   ├── tools/ (ex.: transcribe_video se for comum)
│   └── prompts/
└── tools/ (facilitadores do root agent)
`

---

## 4. Plano de Implementação
1. Refatorar diretórios sem alterar comportamento do pipeline de criação (garantir testes verdes).
2. Criar gents/update/ replicando estrutura do create e adaptar prompts para atualização.
3. Atualizar ido/agent.py com fluxo human-in-loop e novo AgentTool.
4. Expandir SessionState (previous_doc_path, update_plan etc.).
5. Escrever testes para o pipeline update e atualizar doc (	udo_aqui.md, dk_architecture.md, TESTING.md).

---

## 5. Métricas de Sucesso
- Pipeline update consegue ler docx anterior, gerar plano de modificação e produzir novo manual.
- Sessões gravadas diferenciam create vs update e guardam caminhos relevantes.
- Estrutura do repositório segue o padrão do Tutorial 25 (agents-as-a-tool modular, subagentes em pastas próprias).
- Testes automatizados cobrindo o novo fluxo e documentação sincronizada.

---

## 6. Próximos Passos
- Após conclusão, Sprint 3 pode consumir o SQLite para listar criações/atualizações na UI.
- Avaliar personalização adicional (preferências por usuário) e dashboards de telemetria.
