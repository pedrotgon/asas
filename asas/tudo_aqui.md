# Tudo Aqui — Guia Definitivo do Projeto AIDO

Este documento consolida a engenharia de contexto do AIDO. Ele segue o estilo dos tutoriais 04 (Sequential Workflows) e 06 (Multi-Agent Systems), funcionando como fonte de verdade para arquitetura, operacao e manutencao.

---

## 1. Visao Geral
- **Objetivo**: transformar videos de treinamento em manuais `.docx` revisados com tom pedagogico.
- **Stack principal**: Google Agent Development Kit (ADK) + modelos Gemini 2.5 Flash.
- **Arquitetura**: agente conversacional `Aido` (root) que aciona o pipeline sequencial `create` composto por cinco especialistas.
- **Entrada tipica**: caminho absoluto para arquivo de video localizado em `data/entrada` (ou no valor de `AIDO_INPUT_DIR`).
- **Saidas**: transcricoes cacheadas em `data/saida/txt` e manuais finais em `data/saida/docx` (ou valores definidos via variaveis).

---

## 2. Arquitetura de Alto Nivel
```
Usuario -> Aido (Agent) -> AgentTool(create) -> SequentialAgent(create) -> Subagentes -> Ferramentas -> Artefatos
```
1. **Aido (`aido/agent.py`)**
   - Agente LLM Gemini 2.5 Flash.
   - Ferramentas: `AgentTool(agent=create)`.
   - Responsavel por entender a intencao e disparar o pipeline `create`.
2. **Create (`aido/create/agent.py`)**
   - `SequentialAgent` com ordem fixa:
     1. `TranscriptionAgent`
     2. `StructuringAgent`
     3. `MasteringAgent`
     4. `JsonToStringAgent`
     5. `WriterAgent`
3. **Subagentes (`aido/create/subagents/*`)**
   - Cada pasta possui `agent.py` e, quando necessario, subpasta `tools/`.
   - Todos os subagentes LLM usam `gemini-2.5-flash`.
4. **Ferramentas**
   - `transcribe_video`: async, utiliza `faster_whisper` com cache local.
   - `convert_to_json_string`: converte `dict`/JSON em string formatada.
   - `write_docx`: gera manual via `docxtpl` respeitando configuracao de caminhos.
   - `finalize_session`: consolida artefatos e valida o estado salvo em banco.

---

## 3. Estrutura de Pastas Relevantes
`
aido/
├── agent.py
├── config.py
├── db.py
├── state.py
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
├── tools/
│   └── context.py
└── shared/ (reservado para utilitarios futuros)
`

---

## 4. Configuracao e Variaveis de Ambiente
`aido/config.py` centraliza caminhos e cria as pastas de trabalho inspirando-se nos tutoriais. Use as variaveis abaixo para customizar (todas possuem valor padrao relativo ao repo):

| Variavel | Descricao |
| --- | --- |
| `AIDO_DATA_ROOT` | Diretorio raiz para dados (`data/` por padrao). |
| `AIDO_INPUT_DIR` | Pasta de entrada de videos. |
| `AIDO_TRANSCRIPTION_DIR` | Pasta para cache das transcricoes. |
| `AIDO_DOCX_DIR` | Pasta para manuais `.docx`. |
| `AIDO_TEMPLATES_DIR` | Pasta de templates. |
| `AIDO_TEMPLATE_PATH` | Caminho completo para o template `.docx`. |
| `AIDO_BASE_STORAGE` | Pasta raiz da persistencia (SQLite, logs, migracoes). |
| `AIDO_DATABASE_URL` | URL completa para o DatabaseSessionService. |

Mantendo toda a configuracao em variaveis, evitamos caminhos hardcoded e seguimos o checklist de producao do tutorial 25.

---

## 5. Fluxo dos Pipelines
### Create
1. **Input do usuario**: caminho absoluto do video.
2. **TranscriptionAgent**: usa 	ranscribe_video e salva ideo_path/	ranscribed_text.
3. **StructuringAgent**: gera JSON StructuredManual.
4. **MasteringAgent**: refina mantendo estrutura.
5. **JsonToStringAgent**: converte para string JSON formatada.
6. **WriterAgent**: preenche template e grava .docx.
7. **SessionRecorderAgent**: consolida status e caminho final.

### Update
1. **Coleta de contexto (root agent)**: confirma video novo (se houver), caminho do manual anterior .txt/.json e instrucoes do usuario; chama set_update_context.
2. **UpdateTranscriptionAgent**: transcreve novo material.
3. **ContextReaderAgent**: carrega manual anterior com load_manual.
4. **DiffPlannerAgent**: compara transcricao, manual e pedido do usuario, produzindo update_plan.
5. **UpdaterAgent**: aplica o plano gerando JSON estruturado atualizado.
6. **UpdateJsonToStringAgent**: converte o JSON revisado em string.
7. **UpdateWriterAgent**: gera novo .docx mantendo template padrao.
8. **UpdateSessionRecorderAgent**: garante que estado e artefatos persistam no SQLite.

---
---

## 6. Boas Praticas Aplicadas
- **Separacao clara** entre orchestrador (`aido/agent.py`) e pipelines modulares (`aido/agents/create` e `aido/agents/update`).
- **Configuracao centralizada** (`aido/config.py`) evitando caminhos absolutos e viabilizando deploy em diferentes ambientes.
- **Ferramentas com validacao de path** garantindo que operacoes acontecem apenas em diretorios autorizados.
- **Cache controlado** para transcricoes (reduce custo e tempo).
- **Modelo consistente**: todos os agentes LLM usam `gemini-2.5-flash`.
- **Instrucao minimalista para tools**: LLM aciona ferramentas sem precisar de caminhos, evitando erros e reforcando reproducibilidade.
- **Testes inspirados nos tutoriais** validando ordem, output keys e existencia de pastas.
- **Persistencia plugavel**: `DatabaseSessionService` configurado via `AIDO_BASE_STORAGE` e `AIDO_DATABASE_URL`, permitindo inspecao de historico fora da memoria local.


---

## 7. Como Executar
1. **Preparacao**
   - Python 3.9+ e dependencias instaladas.
   - `GOOGLE_API_KEY` configurada (env ou CLI).
   - Videos posicionados em `data/entrada`.
2. **Rodar interface**
   ```powershell
   adk web
   ```
3. **Executar pipeline**
   - Abrir `http://localhost:8000`.
   - Selecionar agente `Aido`.
   - Enviar o caminho absoluto do video na primeira mensagem.
4. **Resultado**
   - A resposta final retorna o caminho do manual `.docx` dentro de `data/saida/docx`.
   - Logs do console mostram execucao das ferramentas (`--- TOOL:`).

---

## 8. Testes e Validacao
- **Testes automatizados**: `pytest tests/test_agents.py`
  - Verifica ordem dos subagentes, `output_key` e resolucao de caminhos.
- **Ciclo manual**:
  1. Adicionar video de exemplo em `data/entrada`.
  2. Executar `adk web` e rodar pipeline.
  3. Aferir se json estruturado e doc gerado respeitam formatacao esperada.
- **Logs**: mensagens das ferramentas indicam cache, erro e sucesso.

---

## 9. Troubleshooting
| Sintoma | Causa Provavel | Acao |
| --- | --- | --- |
| `Security Error` ao transcrever | Caminho fora de `AIDO_INPUT_DIR` | Mover video para diretorio autorizado ou ajustar variavel. |
| Cache nao eh reutilizado | Arquivo nao localizado ou corrompido | Revisar permissao ou remover cache para regerar. |
| `Template file not found` | Template ausente ou variavel incorreta | Confirmar `templates/Padronizacao_Manuais.docx` ou `AIDO_TEMPLATE_PATH`. |
| Saida sem listas formatadas | Instrucoes do structuring/mastering alteradas | Revisar textos dos agentes e restaurar marcadores. |
| Erro `faster-whisper` nao instalado | Dependencia ausente | Instalar `faster-whisper` ou configurar alternativa antes da execucao real. |
| `previous_manual_path` ausente | Usuario nao informou caminho do manual anterior | Orientar o usuario a fornecer arquivo `.txt` ou `.json` e registrar com `set_update_context`. |
| `update_plan` vazio | LLM nao entendeu pedido de atualizacao | Revisar instrucoes repassadas, pedir detalhes adicionais e reexecutar `DiffPlannerAgent`. |
| Sessao nao persiste apos reinicio | `DATABASE_URL` apontando para local temporario ou falta de permissao | Garantir `AIDO_DATABASE_URL`/`AIDO_BASE_STORAGE` apontando para `data/base/sqlite` e que o arquivo `.db` seja acessivel. |

---

## 10. Roadmap
- **Sprint 2**: estado e memoria persistente (consultar `tasks/sprint_2_state_memory.md`).
- **Sprint 3**: interface web customizada.
- **Sprint 4**: empacotamento e deploy seguindo tutorial 25.
- **Observabilidade**: adicionar plugins de metricas e alertas (pendente, ver checklist de producao).
- **Seguranca**: planejar autenticacao e rate limiting antes do deploy externo.

---

## 11. Referencias Cruzadas
- `README.md`: guia rapido de setup.
- `adk_architecture.md`: visao macro da arquitetura (atualizar quando houver mudancas).
- `GEMINI.md`: detalhes da integracao ADK + Gemini e melhores praticas de prompt.
- `tasks/*.md`: planejamento por sprint.
- `adk_training/`: repositorio base dos tutoriais (usado como referencia viva).

---

## 12. Historico Recente
- Centralizacao de paths em `aido/config.py` (substitui caminhos absolutos antigos).
- Atualizacao das ferramentas para usar configuracao dinamica.
- Ajuste das instrucoes do `WriterAgent` para simplificar o uso da ferramenta.
- Inclusao de testes estruturais em `tests/`.
- Revisao geral de documentacao (`README.md` e este guia) alinhando com estrutura atual.

---

## 13. Recomendacoes Operacionais
- Atualizar este guia sempre que a arquitetura mudar (evita divergencia de contexto).
- Agrupar commits por contexto (ex.: "ajusta configuracao de paths" ou "melhora instrucoes do structuring").
- Durante code review, validar consistencia de `output_key`, seguranca de caminhos e aderencia aos tutoriais.
- Antes de deploy, revisar checklist de producao do tutorial 25 (seguranca, metricas, testes).

---

## 14. Contato e Continuidade
- Duvias sobre ADK: consultar `adk_training/docs/` e implementacoes de referencia.
- Questao de arquitetura: revisar `adk_architecture.md` e este documento.
- Bugs/melhorias: registrar em `tasks/` antes de implementar para manter backlog organizado.

---

**Este documento deve ser mantido vivo. Atualize sempre apos cada decisao arquitetural relevante.**
