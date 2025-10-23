# AIDO - Assistente Inteligente de Documentacao

> Consulte a documentacao oficial do ADK (tutorial04 e tutorial06) sempre que for evoluir o projeto.

## Visao Geral

O AIDO transforma videos de treinamento em manuais `.docx`. O fluxo segue o padrao `SequentialAgent` do Tutorial 04, combinado com um agente maestro que expone o pipeline como ferramenta (padrao apresentado no Tutorial 06).

### Componentes principais

- `aido/agent.py`: agente conversacional (`root_agent`) que decide entre criar ou atualizar e registra contexto.
- `aido/agents/create/` e `aido/agents/update/`: pipelines Agent-as-a-Tool, com seus subagentes especializados.
- `aido/config.py`: centraliza configuracoes de caminhos usando variaveis de ambiente.
- `aido/state.py` e `aido/db.py`: persistem o estado das sessoes no SQLite.
- `aido/tools/context.py`: funcoes auxiliares para registrar informacoes de atualizacao.
- `data/`: raiz padrao para arquivos de entrada e saida (`entrada/`, `saida/txt`, `saida/docx`, `base/`).
- `templates/`: armazena o template `Padronizacao_Manuais.docx` utilizado na geracao do manual.
- `tests/`: verificacoes rapidas de estrutura/estado, inspiradas nos tutoriais 04, 06 e 08.

## Configuracao

O projeto usa variaveis de ambiente para evitar caminhos hardcoded. Todas possuem valores padrao relativos a raiz do repositorio.

| Variavel                | Padrao                             | Uso                                  |
|------------------------|-------------------------------------|--------------------------------------|
| `AIDO_DATA_ROOT`       | `<repo>/data`                      | Diretorio pai dos dados              |
| `AIDO_INPUT_DIR`       | `<data>/entrada`                   | Onde ficarão os videos de entrada    |
| `AIDO_TRANSCRIPTION_DIR` | `<data>/saida/txt`               | Cache das transcricoes               |
| `AIDO_DOCX_DIR`        | `<data>/saida/docx`                | Saida final dos manuais              |
| `AIDO_TEMPLATES_DIR`   | `<repo>/templates`                 | Diretorio de templates               |
| `AIDO_TEMPLATE_PATH`   | `<templates>/Padronizacao_Manuais.docx` | Template principal               |
| `AIDO_BASE_STORAGE`    | `<data>/base`                      | Raiz da persistencia (SQLite/logs)   |
| `AIDO_DATABASE_URL`    | `sqlite:///<data/base/sqlite/aido_data.db>` | URL para o DatabaseSessionService |

Para personalizar, crie um arquivo `.env` (ou ajuste o processo de deploy) definindo as variaveis desejadas.

## Requisitos

- Python 3.9 ou superior
- Dependencias do ADK (`pip install -r adk_training/requirements.txt` ou conforme ambiente)
- `GOOGLE_API_KEY` configurada (ADK CLI ou variavel de ambiente)

## Como Executar

### Backend (FastAPI + AG-UI)

1. (Opcional) Crie e ative um ambiente virtual Python.
2. Instale as dependências do AIDO:
   ```bash
   pip install -r aido/requirements.txt
   ```
3. Inicie a API:
   ```bash
   python -m aido
   ```
   O serviço expõe:
   - `GET /api/healthz` — verificação simples
   - `GET /api/sessions` — lista sessões persistidas (usa `DatabaseSessionService`)
   - `POST /api/copilotkit` — endpoint consumido pelo CopilotKit

### Frontend (CopilotKit UI)

1. Entre na pasta `aido/ui`.
2. Instale as dependências JavaScript:
   ```bash
   npm install
   ```
3. Rode em modo desenvolvimento:
   ```bash
   npm run dev
   ```
   A UI abrirá em `http://localhost:5173`, com proxy para `http://localhost:8000/api`.

### Pipelines ADK tradicionais

Se desejar executar via `adk web`, siga o fluxo clássico:

1. Copie o vídeo para `data/entrada`.
2. Execute `adk web` na raiz.
3. No navegador (porta 8000), escolha o agente `Aido` e forneça o caminho absoluto do vídeo.
4. O pipeline gerará a transcrição, os JSONs e o `.docx`, registrando tudo no SQLite (`data/base/sqlite/aido_data.db`).

## Testes

Os testes seguem estratégia em camadas:

- **Python**:
  ```bash
  pytest tests/test_agents.py tests/test_concierge.py
  ```
  (`tests/test_api.py` é executado automaticamente quando `ag_ui_adk` está instalado.)

- **Frontend**:
  ```bash
  cd aido/ui
  npm run test          # Vitest
  npm run test:ui       # Playwright (após subir `npm run dev`)
  ```

Esses testes cobrem o concierge, a configuração do root agent, endpoints FastAPI e componentes principais da UI.

## Documentacao Complementar

- `tudo_aqui.md`: guia operacional e tecnico central do projeto.
- `adk_architecture.md`: diagrama e descricoes de arquitetura.
- `GEMINI.md`: detalhes sobre a integracao com Gemini e ADK.
- Pasta `adk_training/`: referencia completa dos tutoriais originais (utilizada como base de boas praticas).
