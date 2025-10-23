# Sprint 4 – Deploy Produtivo com Guardrails, Observabilidade e TDD

Esta sprint leva a arquitetura AG-UI para produção na Google Cloud Platform, preservando sessão WebSocket, guardrails e telemetria. O foco é assertividade: pipelines de CI/CD, testes automatizados, políticas de segurança e monitoramento para manter o root agent e seus subagentes confiáveis em escala.

---

## 1. Backlog da Tarefa ✅

| ID | Sub-tarefa | Resultado |
| --- | --- | --- |
| S4-T01 | Escrever `Dockerfile` multi-stage (backend FastAPI + `ag-ui-adk`) com steps de testes (pytest) antes do build final. | [ ] |
| S4-T02 | Provisionar GCP (Terraform ou scripts) para Cloud Run, Cloud SQL (Postgres gerenciado), Cloud Storage/CDN e VPC connectors. | [ ] |
| S4-T03 | Configurar `Secret Manager` e `Cloud SQL Auth Proxy`, gerando políticas de rotações e testes automatizados de credenciais. | [ ] |
| S4-T04 | Construir pipeline CI/CD no Cloud Build: lint + testes + build backend + build frontend + publicação de imagens/artefatos. | [ ] |
| S4-T05 | Implantar backend no Cloud Run com afinidade de sessão habilitada, health-check customizado e métricas exportadas (OpenTelemetry). | [ ] |
| S4-T06 | Build do frontend com `VITE_COPILOTKIT_RUNTIME_URL` apontando para o Cloud Run; publicar assets no Cloud Storage + CDN com testes de smoke. | [ ] |
| S4-T07 | Executar migrações Alembic (Cloud Build job) e validar integridade do estado (`SessionState`) em Cloud SQL. | [ ] |
| S4-T08 | Rodar testes e2e em staging/prod (Playwright/Cypress) garantindo loop de aprovação, guardrails e persistência; implementar rollback automatizado. | [ ] |
| S4-T09 | Configurar monitoramento (Cloud Monitoring, Logging, Error Reporting) com alertas para latência, falhas de guardrail e status WebSocket. | [ ] |

---

## 2. Visão Geral da Solução ☁️

- **Frontend**: SPA (Vite/React) hospedada em Cloud Storage + Cloud CDN, versãoada pelo pipeline. Build injeta endpoints de produção e faz teste de integridade (hash).  
- **Backend**: FastAPI + AG-UI rodando em Cloud Run (containers imutáveis). `session affinity` garante WebSocket estável; callbacks reportam métricas a cada fluxo.  
- **Persistência**: Cloud SQL (Postgres) continua como fonte da verdade. Migrações Alembic e seeds são executados via Cloud Build Jobs com testes após cada deploy.  
- **Segurança & Guardrails**: Secrets no Secret Manager, IAM granular, auditoria de callbacks (bloqueios/aprovações) enviada ao Cloud Logging.  
- **TDD em produção**: Build falha se testes unit/integration/e2e não passarem. Testes de fumaça pós-deploy garantem que root agent, concierge e pipelines respondam conforme esperado.

---

## 3. Implementação Detalhada 🔧

1. **Infraestrutura & Configuração**
   - Terraform/Cloud SDK para criar serviços (Cloud Run, Cloud SQL, Storage, CDN) com ambientes dev/staging/prod.  
   - Configurar VPC connectors se necessário (acesso privado ao Cloud SQL).

2. **CI/CD**
   - Etapas: lint → pytest/tests callbacks → build imagem → rodar testes containerizados → build frontend → testes unitários UI → upload para GCS → deploy Cloud Run → rodar Playwright/Cypress.  
   - Artefatos versionados (tags e commit hashes) para rollback rápido.

3. **Runtime**
   - Cloud Run com `max-instances`, `min-instances`, session affinity e health-check GET `/healthz`.  
   - Logs estruturados (JSON) com contexto de sessão, métricas de guardrail e eventos AG-UI.  
   - Exportar métricas via OpenTelemetry/Cloud Monitoring (tempo de resposta, taxa de bloqueio, eventos por sessão).

4. **Testes Pós-Deploy**
   - Playwright/Cypress em ambiente staging e produção (smoke) garantindo chat, aprovações, guardrails.  
   - Scripts que validam a existência de registros em Cloud SQL após pipelines completos.

---

## 4. Boas Práticas Aplicadas ⭐

- Infraestrutura como Código e CI/CD declarativo.  
- Segurança: segredos rotacionados, papéis mínimos, Cloud Armor opcional para proteger endpoints.  
- Observabilidade: dashboards e alertas por componente (latência, erros callbacks, falhas WebSocket).  
- TDD: pipelines só prosseguem com cobertura mínima, testes e2e e smoke automatizados.  
- Estratégia de rollback (versões anteriores do Cloud Run + objetos CDN versionados).

---

## 5. Checklist de Entrega ✅

- [ ] Pipelines CI/CD executam testes e builds sem intervenção manual.  
- [ ] Cloud Run serve backend com session affinity e health-checks verdes.  
- [ ] UI distribuída via CDN e responde com assets corretos.  
- [ ] Loop concierge → aprovação → pipeline funciona em produção sob WebSockets estáveis.  
- [ ] Guardrails registram métricas e bloqueios no Monitoring/Logging.  
- [ ] Cloud SQL contém registros consistentes pós-pipeline (validados por scripts).  
- [ ] Playwright/Cypress em staging/prod aprovados; rollback documentado.  
- [ ] Documentação de operação/deploy publicada (README/TESTING/Runbook).

---

## 6. Próximos Passos 🔄

- Configurar domínio customizado + certificados gerenciados (Cloud Load Balancer + CDN).  
- Expandir observabilidade (dashboards executivos, alertas por canal).  
- Planejar Sprint 5: métricas avançadas, agentes de QA automáticos, acessibilidade contínua.

---

## 7. Referências 📚

- GCP: [Session affinity Cloud Run](https://cloud.google.com/run/docs/configuring/session-affinity), [Static hosting Cloud Storage](https://cloud.google.com/storage/docs/hosting-static-website)  
- ADK/AG-UI: `tasks/sprint_3_ui.md`, `adk_training/docs/docs/09_callbacks_guardrails.md`, `adk_training/docs/docs/30_nextjs_adk_integration.md`  
- Pesquisa: `adk_training/research/adk_ui_integration/02_ag_ui_framework_research.md`, `03_nextjs_react_vite_research.md`
