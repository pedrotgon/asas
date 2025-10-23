# AIDO — Estratégia de Testes End-to-End

Este guia reúne as práticas recomendadas para testar o AIDO após a Sprint 2. Ele combina as orientações dos tutoriais ADK (especialmente 04, 06, 08, 19 e 25) com o planejamento das próximas sprints.

---

## 1. Pirâmide de Testes Adaptada ao AIDO
| Camada | Objetivo | Exemplos | Frequência |
| --- | --- | --- | --- |
| **Unitários** | Validar funções puras e ferramentas. | 	ranscribe_video com mocks, write_docx gerando arquivo temporário, utilitários do SessionState. | CI a cada commit. |
| **Arquiteturais** | Garantir wiring entre agentes/tooling. | 	ests/test_agents.py valida ordem do pipeline, 	ests/test_state.py garante serialização do estado. | CI a cada commit. |
| **Integração** | Exercitar os pipelines create e update em ambiente controlado. | Rodar create/update com vídeo curto e base SQLite temporária (`tmp_path`). | Semanal ou antes de merge crítico. |
| **Avaliações ADK** | Medir qualidade de saída usando eval_sets. | dk eval com vídeos reais e métricas de consistência. | A cada sprint ou antes de release. |
| **Produção / Smoke** | Confirmar deploy, autenticação, métricas. | dk web em staging + monitoramento/KPI. | A cada release. |

---

## 2. Testes Técnicos por Componente
### 2.1 Ferramentas (	ools)
- **Transcrição**: mockar WhisperModel (pytest + monkeypatch). Verificar:
  - Respeito a AIDO_INPUT_DIR (paths inválidos → Security Error).
  - Reuso do cache em AIDO_TRANSCRIPTION_DIR.
  - Atualização de 	ool_context.state (ideo_path, status=in_progress).
- **Conversão JSON**: inputs inválidos (string quebrada, objeto sem model_dump) geram mensagens claras.
- **Geração .docx**:
  - Template inexistente → mensagem de erro.
  - Caminhos fora de AIDO_DOCX_DIR → erro de segurança.
  - Conteúdo final (usar python-docx para inspecionar headings/listas).
  - Estado atualizado (generated_docx_path, status).

### 2.2 Subagentes
- Fixtures fixas inspiradas em 	utorial04/	utorial06.
  - **Structuring/Mastering**: validar JSON com StructuredManual (Pydantic).
  - **SessionRecorder**: verificar que inalize_session escreve session_id, status, updated_at.

### 2.3 Pipelines create e update
- **Create**: executar com vídeo pequeno (sample_files/ ou `data/entrada/...`). Verificar estado completo, caminho final e erros comuns (vídeo ausente, JSON inválido).
- **Update**: fornecer manual anterior (`previous_manual_path`) e pedido de alteração. Conferir geração de `update_plan`, JSON revisado e novo DOCX.
- Para ambos, revisar logs `--- TOOL:` e validar persistência no SQLite (`data/base/sqlite/aido_data.db`).

---

## 3. Estratégia por Sprint
### Sprint 1 (histórico)
- Cobertura básica com 	ests/test_agents.py + unitários das ferramentas.

### Sprint 2 — Estado & Memória (atual)
- 	ests/test_state.py cobre roundtrip do SessionState e verifica que session_service é do tipo DatabaseSessionService.
- Testes de integração devem simular reinício: executar pipeline, reiniciar runner e confirmar que o estado pode ser lido da base.
- Monitorar crescimento do arquivo .db e criar fixture que usa 	mp_path para instâncias temporárias.

### Sprint 3 — UI Custom
- Playwright/automação para upload de vídeos, visualização de sessões.
- Contratos HTTP com TestClient do FastAPI (autenticação + rate limiting).
- Testes de acessibilidade (xe-core, pa11y).

### Sprint 4 — Deploy & Observabilidade
- Smoke tests pós-deploy (health check, rota principal, conexão ao banco).
- Testes de carga (locust, k6) simulando múltiplos usuários.
- Segurança: rate limiting, chaves inválidas, isolamento das ferramentas.
- Observabilidade: validar métricas e alertas dos plugins ADK.

---

## 4. Boas Práticas Complementares
1. Fixar seeds para reduzir variabilidade (google.adk.utils.seed).
2. Versionar snapshots de JSON e .docx (detecção de regressões).
3. Utilizar ambientes/.env isolados por sprint.
4. Registrar falhas no arquivo de sprint correspondente (	asks/*.md).
5. Automatizar CI/CD com lint, pytest, pytest --cov, dk eval leve e upload de artefatos.
6. Manter biblioteca de vídeos sintéticos livres para regressões frequentes.

---

## 5. Ferramentas & Scripts Sugeridos
- pytest, pytest-asyncio, pytest-cov.
- coverage html para monitorar evolução (meta ≥ 80% em ferramentas e estado).
- dk eval com conjuntos de cenários.
- pre-commit para padronização (black, isort, flake8).
- make/Taskfile com comandos (make test-unit, make test-integration).

---

## 6. Roteiro de Execução Rápido
`ash
# 1. Unitários + arquiteturais
pytest tests/test_agents.py tests/test_state.py

# 2. Integração em memória (vídeo pequeno + base temporária)
pytest tests/integration/test_create_pipeline.py

# 3. Avaliação (pré-release)
adk eval --agent aido --eval-set eval_sets/sprint2.json --save-report reports/sprint2.json
`

---

## 7. Checklist Pré-Release
- [ ] Testes unitários/arquiteturais verdes (pytest tests/test_agents.py tests/test_state.py).
- [ ] Pipeline validado com ≥ 2 vídeos reais e registro correspondente no SQLite.
- [ ] Relatório dk eval acima das metas definidas.
- [ ] Logs e alertas verificados (data/base/logs).
- [ ] Documentação sincronizada (	udo_aqui.md, dk_architecture.md, 	asks/sprint_2_state_memory.md).
- [ ] Plano de rollback descrito (Tutorial 25).

Mantendo esta disciplina a cada sprint garantimos qualidade contínua e aderência às melhores práticas do ADK.
