# Sprint 1 — Migração para Arquitetura ADK Sequencial

Este documento funciona como o `/docs` oficial da Sprint 1. Ele consolida o que planejamos, executamos e aprendemos durante a migração do AIDO para a arquitetura recomendada pelo ADK, utilizando o estilo de documentação dos tutoriais de agentes (`AGENTS.md` como referência).

---

## 1. Backlog da Sprint 📋

| ID | Tarefa | Resultado |
| --- | --- | --- |
| S1-T01 | Mapear arquitetura alvo baseada em `SequentialAgent` | ✅ |
| S1-T02 | Refatorar agentes e ferramentas para a nova estrutura modular (`aido/create/subagents/...`) | ✅ |
| S1-T03 | Encapsular pipeline `create` como `AgentTool` do agente conversacional `Aido` | ✅ |
| S1-T04 | Eliminar caminhos hardcoded e centralizar configuração de diretórios | ✅ |
| S1-T05 | Atualizar documentação de referência (`README.md`, `tudo_aqui.md`, `adk_architecture.md`, `AGENTS.md`) | ✅ |
| S1-T06 | Criar testes de sanidade inspirados nos tutoriais 04 e 06 | ✅ |

---

## 2. Visão Geral da Solução 🚀

- **Arquitetura**: `Aido` (Agent) expõe o pipeline sequencial `create` como ferramenta (`AgentTool`), alinhado às boas práticas dos tutoriais 04 e 06.  
- **Pipeline `create`**: executa, nesta ordem, `TranscriptionAgent`, `StructuringAgent`, `MasteringAgent`, `JsonToStringAgent` e `WriterAgent`, cada um com `output_key` único.  
- **Configuração**: `aido/config.py` centraliza a resolução de caminhos (entrada, cache, templates, saída) com suporte a variáveis de ambiente (`AIDO_DATA_ROOT`, etc.).  
- **Ferramentas críticas**: `transcribe_video` e `write_docx` usam os caminhos configurados, validam diretórios permitidos e registram logs detalhados.  
- **Documentação viva**: `README.md`, `tudo_aqui.md`, `adk_architecture.md` e `AGENTS.md` foram reescritos para refletir a nova arquitetura e orientar qualquer membro da equipe.

---

## 3. Implementação Detalhada 🧱

### 3.1 Estrutura de Código
| Item | Descrição |
| --- | --- |
| `aido/agent.py` | Agente conversacional que aciona o pipeline via `AgentTool(create)`. |
| `aido/create/agent.py` | `SequentialAgent` que organiza os subagentes em ordem fixa. |
| `aido/create/subagents/*/agent.py` | Especialistas seguindo o padrão dos tutoriais (prompt objetivo, `output_key`, uso de ferramentas). |
| `aido/create/subagents/*/tools/*.py` | Ferramentas assíncronas com validação de caminhos. Agora possuem `__init__.py` para facilitar imports. |
| `aido/config.py` | Resolve caminhos padrão, permite overriders via variáveis e cria diretórios necessários. |
| `tests/test_agents.py` | Teste rápido que garante ordem do pipeline, `output_key` corretos e existência dos diretórios configurados. |

### 3.2 Fluxo de Execução
1. Usuário envia o caminho absoluto do vídeo na primeira mensagem.  
2. `Aido` confere o pedido e chama o pipeline `create`.  
3. `TranscriptionAgent` chama `transcribe_video`, reutilizando cache (`data/saida/txt`).  
4. `StructuringAgent` monta JSON conforme `StructuredManual`.  
5. `MasteringAgent` refina mantendo chaves originais.  
6. `JsonToStringAgent` converte para string JSON identada.  
7. `WriterAgent` usa `write_docx` (template e diretório parametrizados). Resultado final: caminho do `.docx` em `data/saida/docx`.  
8. Resposta enviada ao usuário com o caminho gerado.

---

## 4. Problemas Encontrados e Correções 🔧

| Situação | Causa | Correção |
| --- | --- | --- |
| `"Fail to load 'aido' module. No module named 'aido.create.subagents.json_converter.tools'"` | Subpasta denominada `tool/` em vez de `tools/` | Ajuste da importação (`json_converter/agent.py`) e criação de `__init__.py` nos diretórios de tools. |
| Ferramentas com caminhos absolutos para usuário específico | Código herdado do protótipo antigo | Criação do módulo `aido/config.py` e uso das variáveis `AIDO_*` em todas as ferramentas. |
| Falta de init em diretórios de ferramentas | Python não tratava a pasta como pacote | Inclusão de `__init__.py` em `transcription/tools`, `writer/tools`, `json_converter/tool`. |
| Execução de `pytest` rodando testes de todo o repositório de treinamento | `pytest` sem argumento varreu `adk_training` | Documentado que devemos rodar `pytest tests/test_agents.py` para validar apenas o AIDO. |
| Textos divergentes em documentação (referências a `new/`) | Conteúdo herdado do repositório original | `README.md`, `tudo_aqui.md`, `adk_architecture.md` e `AGENTS.md` reescritos com a nova estrutura. |

---

## 5. Boas Práticas Aplicadas ✅

- **Configuração via ambiente**: nenhum caminho hardcoded; tudo passa por `aido/config.py`.  
- **Ferramentas assíncronas**: `asyncio.to_thread(...)` para transcrição e geração de `.docx`, evitando bloqueio.  
- **Logs pedagógicos**: mensagens `--- TOOL:` seguem o padrão do tutorial 06, facilitando depuração.  
- **Documentação viva**: `tudo_aqui.md` e `adk_architecture.md` servem como gêmeos digitais.  
- **Testes de sanidade**: cobertura minimalista inspirada no Tutorial 04 para garantir ordem e dependências básicas.  
- **Prompt design**: prompts focados em saída determinística (JSON, Markdown) e tom pedagógico, como documentado em `AGENTS.md`.

---

## 6. Checklist de Entrega da Sprint 📦

- [x] Pipeline `create` funcional via `adk web`.
- [x] `Aido` responde conversas e aciona o pipeline conforme esperado.
- [x] Geração de manuais `.docx` em `data/saida/docx` com template padrão.
- [x] Variáveis `AIDO_*` documentadas e com defaults seguros.
- [x] Teste `pytest tests/test_agents.py` criado (executar isoladamente).
- [x] Documentação revisada (README, `tudo_aqui.md`, `adk_architecture.md`, `AGENTS.md`).  

---

## 7. Próximos Passos (Entrada para Sprint 2) 🔮

1. **Estado & Memória**: Persistir `session_state` em armazenamento durável.  
2. **Segurança**: Implementar autenticação, rate limiting e plugins de observabilidade (checklist do Tutorial 25).  
3. **Experiência de Usuário**: Planejar UI customizada (Sprint 3).  
4. **Deploy**: Preparar automação e monitoramento para ambiente gerenciado (Sprint 4).  

---

## 8. Referências Cruas 📚

- `AGENTS.md`: guia de prompts e uso dos modelos.  
- `tudo_aqui.md`: manual operacional completo do pipeline.  
- `adk_architecture.md`: diagrama e descrição atualizados.  
- `tests/test_agents.py`: validação rápida da estrutura.  
- Tutoriais: 04 (Sequential Workflows), 06 (Multi-Agent Systems), 25 (Best Practices).  

---

**Sprint 1 concluída com sucesso.** A fundação do AIDO está sólida, pronta para receber memória persistente, segurança reforçada e melhorias de UX nas próximas sprints.  
