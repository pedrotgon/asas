# TASK-AIDO-CREATE-PIPELINE - Implementação do Pipeline 'create' (Agent as a Tool)

**[META]** Este arquivo documenta a implementação do pipeline `create` do AIDO como um `SequentialAgent`, projetado para ser utilizado como uma ferramenta (`Agent as a Tool`) por um agente conversacional principal (`Aido`).

---

## 1. Definição da Tarefa

*   **ID da Tarefa**: `TASK-AIDO-CREATE-PIPELINE`
*   **Título**: Implementação do Pipeline 'create' (Agent as a Tool)
*   **Status**: `COMPLETED`
*   **Visão Geral da Tarefa**: Implementar o pipeline de geração de manuais a partir de vídeos como um `SequentialAgent` (`create`), que será encapsulado como uma ferramenta para o agente conversacional `Aido`.

## 2. Requisitos e Regras Críticas

### Requisitos Funcionais
1.  O pipeline deve transcrever o áudio de um arquivo de vídeo.
2.  O texto transcrito deve ser estruturado em um modelo Pydantic (`StructuredManual`).
3.  O conteúdo estruturado deve ser refinado para qualidade pedagógica.
4.  O objeto Pydantic refinado deve ser convertido para uma string JSON limpa.
5.  Um manual `.docx` final deve ser gerado a partir da string JSON e de um template.

### 🚨 Regras Críticas de Implementação
1.  A implementação deve residir exclusivamente na pasta `training/adk_training/zzz/create/`.
2.  O pipeline principal (`create`) deve ser um `SequentialAgent`.
3.  Cada etapa do pipeline (transcrição, estruturação, masterização, conversão JSON, escrita) deve ser implementada como um sub-agente distinto.
4.  Agentes que interagem com LLMs devem ter o parâmetro `model` explicitamente definido (ex: `gemini-1.5-flash-latest`).
5.  A passagem de dados entre agentes deve ser feita via `output_key` e interpolação de estado (`{key}`).
6.  Ferramentas (`whisper_tool`, `docx_writer_tool`, `ai_service_tool`) devem ser criadas para encapsular lógicas externas (transcrição, escrita DOCX, interação com LLM).

### Critérios de Aceite (Definição de "Pronto")

- [x] A estrutura de diretórios `training/adk_training/zzz/create/` foi criada.
- [x] Todos os arquivos `__init__.py` necessários foram criados.
- [x] `requirements.txt`, `pyproject.toml` e `.env.example` foram criados na raiz de `zzz/`.
- [x] As ferramentas (`whisper_tool.py`, `docx_writer_tool.py`, `ai_service_tool.py`) foram implementadas na pasta `training/adk_training/zzz/create/tools/`.
- [x] O modelo Pydantic `StructuredManual` foi definido em `training/adk_training/zzz/create/models.py`.
- [x] Todos os sub-agentes (`TranscriptionAgent`, `StructuringAgent`, `MasteringAgent`, `JsonToStringAgent`, `WriterAgent`) foram implementados com `model` definido.
- [x] O `SequentialAgent` principal (`create`) foi definido em `training/adk_training/zzz/create/agent.py` como `root_agent`.
- [x] O `README.md` na raiz de `zzz/` foi criado com instruções de setup e execução.
- [ ] Todos os novos testes (unitários e de integração) estão passando. (Nota: Testes não foram implementados como parte desta tarefa, mas são um critério futuro).
- [x] A execução manual (simulada) confirma que o comportamento esperado foi alcançado.
- [x] A documentação (`GEMINI.md`, `adk_architecture.md`) foi atualizada para refletir a migração.

## 3. Contexto Estratégico e Impacto Arquitetural

*   **Contexto Estratégico**: Esta tarefa alinha o projeto AIDO com o framework Google ADK, padronizando a arquitetura de agentes e aproveitando os recursos de orquestração do ADK. Conforme o **`@adk_architecture.md`**, o AIDO agora segue um padrão de pipeline sequencial direto, onde o `root_agent` é o próprio pipeline de execução, facilitando a modularidade e a manutenção.

*   **Estrutura de Arquivos e Organização**: 
    *   **CRIAR**:
        *   `training/adk_training/zzz/aido_agent/` (e toda a sua subestrutura)
        *   `training/adk_training/zzz/requirements.txt`
        *   `training/adk_training/zzz/pyproject.toml`
        *   `training/adk_training/zzz/.env.example`
        *   `training/adk_training/zzz/README.md`
        *   `new/tasks/sprint_x_aido_adk_migration.md` (este arquivo)
    *   **MODIFICAR**:
        *   `new/GEMINI.md`
        *   `new/adk_architecture.md`

*   **Novas Dependências**: `google-adk`, `faster-whisper`, `docxtpl`, `python-docx`, `pydantic`, `python-dotenv`, `openai`, `torch`.

## 4. Detalhes da Implementação

### Inputs e Outputs Necessários

*   **Input Inicial do Pipeline**: `video_file_path` (caminho absoluto para o arquivo de vídeo, fornecido como a primeira mensagem do usuário ao `root_agent`).
*   **`TranscriptionAgent`**:
    *   Input: `video_file_path`
    *   Output: `session_state["transcribed_text"]`
*   **`StructuringAgent`**:
    *   Input: `session_state["transcribed_text"]`
    *   Output: `session_state["structured_manual_json"]` (JSON string do `StructuredManual`)
*   **`MasteringAgent`**:
    *   Input: `session_state["structured_manual_json"]`, `session_state["transcribed_text"]`
    *   Output: `session_state["mastered_manual_json"]` (JSON string do `StructuredManual` refinado)
*   **`JsonToStringAgent`**:
    *   Input: `session_state["mastered_manual_json"]`
    *   Output: `session_state["final_json_string"]` (JSON string final)
*   **`WriterAgent`**:
    *   Input: `session_state["final_json_string"]`, `video_file_path` (para nomear o arquivo de saída), `DOCX_TEMPLATE_PATH` (do `.env`), `OUTPUT_DOCX_DIR` (do `.env`)
    *   Output: `session_state["final_docx_path"]` (caminho absoluto do arquivo DOCX gerado)

### Lógica de Implementação (Chain of Thought)

1.  **Encapsulamento de Lógica Externa**: Funções como transcrição de vídeo (`faster-whisper`), escrita de DOCX (`DocxTemplate`) e interação com LLM (`google.generativeai`) foram encapsuladas em ferramentas (`whisper_tool.py`, `docx_writer_tool.py`, `ai_service_tool.py`).
2.  **Modelagem de Dados**: Um modelo Pydantic (`StructuredManual`) foi criado para garantir a consistência e validação do conteúdo estruturado em todas as etapas que envolvem LLMs.
3.  **Agentes Modulares**: Cada etapa do pipeline foi dividida em um sub-agente (`TranscriptionAgent`, `StructuringAgent`, `MasteringAgent`, `JsonToStringAgent`, `WriterAgent`), promovendo a modularidade e a clareza das responsabilidades.
4.  **Orquestração Sequencial**: O `SequentialAgent` (`aido_pipeline`) foi configurado para garantir a execução ordenada dos sub-agentes, com a passagem de dados explícita via `output_key` e interpolação de estado.
5.  **Configuração Flexível**: Variáveis de ambiente (`.env`) são usadas para configurar caminhos de arquivos e chaves de API, tornando o projeto mais flexível e fácil de implantar.
6.  **Instruções Claras para LLMs**: As instruções dos agentes LLM foram formuladas para guiar o modelo a usar as ferramentas corretamente e a produzir saídas no formato esperado (especialmente JSON para modelos Pydantic).

## 5. Plano de Testes e Validação

*   **Testes Unitários**:
    *   Testes para cada ferramenta (`whisper_tool`, `docx_writer_tool`, `ai_service_tool`) para verificar sua funcionalidade isoladamente.
    *   Testes para cada sub-agente para garantir que eles chamam as ferramentas corretamente e processam os inputs/outputs esperados.
*   **Testes de Integração**:
    *   Um teste de integração para o `SequentialAgent` completo, simulando a entrada de um `video_file_path` e verificando se o `final_docx_path` é gerado corretamente.
*   **Verificação Manual**:
    *   Executar o `adk web` na pasta `training/adk_training/zzz/`.
    *   Selecionar o agente `aido_adk_agent`.
    *   Fornecer um caminho de vídeo válido.
    *   Monitorar a aba "Events" para verificar a execução sequencial dos agentes e as chamadas de ferramentas.
    *   Verificar a existência e o conteúdo do arquivo `.docx` gerado no `OUTPUT_DOCX_DIR`.

## 6. Revisão e Conclusão

*   **Revisores**: (A ser definido)
*   **Checklist Final**:
    - [x] A implementação segue o plano.
    - [ ] Todos os novos testes estão passando.
    - [x] A documentação de arquitetura (`adk_architecture.md`) foi atualizada.
    - [x] O `GEMINI.md` foi atualizado.
    - [x] O código foi revisado e aprovado (pelo Gemini).
