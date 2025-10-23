# Arquitetura AIDO — Sprint Bônus (Create & Update)

Esta arquitetura reflete a reorganização do AIDO para suportar pipelines de criação e atualização seguindo o padrão Agent-as-a-Tool do ADK.

---

## 1. Visão Geral
- **Root**: ido/agent.py conversa com o usuário, decide entre criação ou atualização e registra contexto (incluindo update_request).
- **Pipelines**:
  - create_tool → create_pipeline (SequentialAgent) gera manuais do zero.
  - update_tool → update_pipeline atualiza manuais existentes.
- **Persistência**: DatabaseSessionService (ido/db.py) grava sessões no SQLite (data/base/sqlite).
- **Estado**: SessionState (ido/state.py) armazena artefatos de criação e campos de atualização (manual anterior, plano, etc.).

### Fluxo Geral
`
Usuário
  │
  ├─> Aido (root) ── create_tool ── create_pipeline ──> DOCX novo
  │
  └─> Aido (root) ── set_update_context ── update_tool ── update_pipeline ──> DOCX atualizado
`

---

## 2. Estrutura de Pastas
`
aido/
├── agent.py
├── agents/
│   ├── create/
│   │   ├── tool.py
│   │   └── pipeline/
│   │       ├── agent.py
│   │       └── subagents/{transcription, structuring, mastering,
│   │                     json_converter, writer, session_recorder}
│   └── update/
│       ├── tool.py
│       └── pipeline/
│           ├── agent.py
│           └── subagents/{transcription, context_reader, diff_planner,
│                         updater, json_converter, writer, session_recorder}
├── tools/context.py   # funções auxiliares para root agent
├── config.py, db.py, state.py
└── ...
`

---

## 3. Pipeline Create
1. **TranscriptionAgent** → 	ranscribe_video
2. **StructuringAgent** → gera JSON conforme StructuredManual
3. **MasteringAgent** → refina mantendo estrutura
4. **JsonToStringAgent** → string JSON formatada
5. **WriterAgent** → aplica template Docx
6. **SessionRecorderAgent** → persiste status e caminhos

## 4. Pipeline Update
1. **UpdateTranscriptionAgent** → texto do novo material
2. **ContextReaderAgent** + load_manual → carrega manual anterior
3. **DiffPlannerAgent** → plano update_plan
4. **UpdaterAgent** → JSON atualizado (StructuredManual)
5. **UpdateJsonToStringAgent** → string JSON
6. **UpdateWriterAgent** → gera DOCX atualizado
7. **UpdateSessionRecorderAgent** → registra resultados

---

## 5. Estado & Persistência
- SessionArtifacts armazena ideo_path, previous_manual_path, update_plan, etc.
- SessionState.to_tool_state() e .from_tool_state() permitem salvar/restaurar no SQLite.
- set_update_context (tool) injeta previous_manual_path e update_request antes do pipeline update.

---

## 6. Observabilidade
- Sessões e eventos persistidos (data/base/sqlite/aido_data.db).
- Estrutura pronta para futuros dashboards/alertas (Sprint 3/4).

---

## 7. Próximos Passos
- UI pode listar sessões e diferenciar criação x atualização.
- Expandir memória de usuário (nome, preferências) e personalizar prompts.
- Instrumentar métricas/alertas conforme checklist do Tutorial 25.
