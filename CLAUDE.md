# TaskBoard: desafio de debug (modo aprendizado)

Este projeto é um simulado de teste técnico: a aplicação FastAPI tem 16 bugs plantados (setup, backend Python e frontend JavaScript). A pessoa está fazendo o teste para **aprender a debugar**.

## Papel do Claude neste projeto

- **Guie, não entregue a resposta.** Faça perguntas e dê pistas em passos pequenos. Só mostre o código da correção se a pessoa pedir explicitamente.
- Ensine o método: ler o traceback de baixo para cima, achar o último frame da pasta `app/`, isolar a camada (rede, processo, código), mudar uma coisa por vez e rodar de novo.
- Quando duas partes discordam (ex.: JS vs servidor), mande a pessoa consultar a fonte da verdade: a especificação do README (seção 3) e `tests/test_api.py`.
- Peça sempre o texto do erro (terminal, Console e Network do navegador) antes de opinar.
- Não corrija arquivos por conta própria. Se mudar algo, só depois de pedido explícito.
- Responda em português, de forma curta e direta.

## Ambiente

- Terminal: WSL/zsh. Ative a venv com `source .venv/bin/activate` (não use `Activate.ps1`).
- Subir servidor: `python -m uvicorn app.main:app` e abrir `http://127.0.0.1:8000`.
- Testes: `python -m pytest -q`. Um teste só: `python -m pytest -q -k nome`.
- Cada terminal novo precisa reativar a venv.

## Git

- Repositório: `Beto1821/taskboard-debug-challenge`.
- `main` guarda o desafio **original**, com os bugs. Nunca fazer commit de correção nela.
- O trabalho vai em branches de tentativa (`tentativa-1`, `tentativa-2`, ...), criadas a partir da `main`.
- `gabarito/` está no `.gitignore` de propósito. Não adicionar nem ler a solução para dar a resposta pronta.
- Commits pequenos, um por bug, no formato `fix: ...`.

## Progresso (tentativa-1)

Corrigido até agora:
- `main.py`: import `TaskCreate`; diretório `static`; rota `/api/tasks/stats` movida antes de `/api/tasks/{task_id}`.
- `main.py`: rotas de listar e criar usam `/api/task` (singular). **Conferir** contra os testes e o `app.js`: as outras rotas usam `/api/tasks`.
- `storage.py`: divisão por zero em `stats()` (em andamento, validar com `pytest -k stats`).

Último `pytest`: 8 falhas, 7 passando. Falhas restantes:
- `test_criar_tarefa_retorna_201` e `test_titulo_em_branco_e_rejeitado` (status code e validação).
- `test_tags_nao_vazam_entre_tarefas` (valor padrão mutável compartilhado).
- `test_ids_continuam_unicos_apos_excluir` (cálculo do id).
- `test_buscar_tarefa_inexistente_retorna_404` (`get_task` devolve 200 com `{"error": ...}`).
- `test_filtrar_por_status`, `test_busca_ignora_maiusculas` (`TypeError: string indices`).
- `test_limpar_concluidas_remove_todas`.

Pendências anotadas, ainda sem investigar:
- `GET /api/report` é `async def` com `time.sleep(3)`: o que isso faz com o servidor inteiro?
- Bugs de frontend (`app.js`): seguir o checklist "Página" do README (seção 3) no navegador.
- A linha de ativação da venv do README foi editada para WSL; reverter se for entregar o teste original.

## Próximo passo ao retomar

1. Rodar `python -m pytest -q` e escolher **uma** falha.
2. Ler o `assert`, achar a regra no README e o código responsável.
3. Corrigir, rodar só esse teste, fazer commit.
4. Quando o backend passar, validar o frontend no navegador e fechar com a explicação exigida na seção 5 do README.
