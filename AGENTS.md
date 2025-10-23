# Integracao ADK + Gemini para o Projeto AIDO

Este guia resume como o AIDO utiliza o Google ADK com modelos Gemini, seguindo as melhores praticas demonstradas nos tutoriais.

## 1. Modelos Utilizados
- Todos os agentes LLM (conversacional + especialistas) utilizam gemini-2.5-flash.
- Escolha motivada por custo/performance durante o treinamento. A troca de modelo deve ser feita de forma centralizada ao ajustar cada agente.

## 2. Configuracao de Credenciais
- Defina GOOGLE_API_KEY no ambiente (arquivo .env ou secret manager).
- Para execucao local com dk web, a chave pode ficar em .env na raiz do projeto.
- Em producao, mover para gerenciador de segredos (Tutorial 25).

## 3. Padroes de Uso no Projeto
| Agente | Tipo | Insercao de contexto |
| --- | --- | --- |
| Aido | Agent | Prompt orientado a entender pedidos e usar create como ferramenta. |
| StructuringAgent | Agent | Prompt injeta {{transcribed_text}} e define formato JSON (Pydantic). |
| MasteringAgent | LlmAgent | Prompt injeta JSON estruturado e transcricao para refinamento. |
| JsonToStringAgent | Agent | Usa ferramenta deterministica; evita respostas livres. |
| WriterAgent | Agent | Aciona write_docx com structured_data; nao precisa conhecer paths. |
| SessionRecorderAgent | Agent | Consolida SessionState, atualiza status e garante persistencia antes de encerrar a sessao. |

Notas importantes inspiradas nas referencias:
- Prompts especificam formato de saida para permitir validacao automatica (tutorial04).
- Passagem de estado ocorre via output_key; cada agente grava apenas uma chave (tutorial06).
- Ferramentas pesadas (	ranscribe_video, write_docx) sao assincronas para nao bloquear a orquestracao.

## 4. Boas Praticas de Prompt
1. **Claridade de papel**: cada prompt comeca definindo o papel do agente (pesquisa, estruturacao, revisao, fechamento).
2. **Formato estrito**: uso de listas, JSON e Markdown explicitamente, evitando interpretacoes livres.
3. **Sem caminhos hardcoded**: gracas ao modulo de configuracao, os prompts do Writer/SessionRecorder nao carregam paths fixos.
4. **Tom pedagogico**: orientado ao usuario final para manter consistencia (parte do diferencial do projeto).

## 5. Debug e Observabilidade
- Use dk web para inspecionar a aba "Events" e ver cada mensagem trocada no pipeline.
- Logs de ferramentas (--- TOOL:) mostram parametros usados e sucesso/erro.
- Com a Sprint 2, o estado persiste em SQLite; e possivel inspecionar data/base/sqlite/aido_data.db para auditar execucoes.
- Planejar instrumentacao de metricas/alertas via plugins ADK (backlog de observabilidade).

## 6. Referencias
- Tutorial 04: Sequential Workflows
- Tutorial 06: Multi-Agent Systems
- Tutorial 08: State & Memory
- Tutorial 25: Best Practices (checklist de producao)
- Documentacao oficial: <https://google.github.io/adk-docs/>
