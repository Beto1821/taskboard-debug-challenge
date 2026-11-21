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

Corrigido até agora (commits em `origin/tentativa-1`):
- `main.py`: import `TaskCreate`; diretório `static`; rota `/api/tasks/stats` antes de `/api/tasks/{task_id}`.
- `main.py` + `app.js`: GET de listar agora `/api/tasks` (plural) nos dois lados (`f4a5f4f`).
- `app.js`: toggle usa `PATCH`, igual ao servidor e aos testes (`4318a8d`).
- `main.py`: `status_code=201` no POST de criar (`3313628`).
- `models.py`: `raise ValueError(...)` no validador de título (`c1397d0`).
- `storage.py`: divisão por zero em `stats()`.
- `storage.py`: `tags=None` em `add` em vez de `tags=[]` (`c247cb2`).

Último `pytest`: 5 falhas, 10 passando. Falhas restantes:
- `test_ids_continuam_unicos_apos_excluir` (`IDs repetidos: [2, 3, 3]`: cálculo do id).
- `test_buscar_tarefa_inexistente_retorna_404` (`ResponseValidationError`: `get_task` devolve 200 com `{"error": ...}`).
- `test_filtrar_por_status`, `test_busca_ignora_maiusculas` (`assert [] == [...]`: `find` em `storage.py` devolve lista vazia; a rota já funciona).
- `test_limpar_concluidas_remove_todas` (removeu 2 em vez de 4).

Lições da sessão (reforçar ao guiar):
- Teste e README são a fonte da verdade; teste nunca muda (já houve edição de teste por engano).
- Mensagem de erro mudou = avanço.
- `/docs` mostra as rotas que o servidor *tem*; o bug é a diferença para o README.
- Ler o `E` do pytest, ignorar `warnings summary` (`httpx2` é ruído). Servidor sem `--reload` roda código antigo.
- `raise` lança erro em Python; `ValueError(...)` sozinho só cria o objeto.
- Git: `git add <arquivos>` antes de `commit`; `git push origin tentativa-1`. Não commitar `tests/`.

Pendências anotadas, ainda sem investigar:
- `GET /api/report` é `async def` com `time.sleep(3)`: o que isso faz com o servidor inteiro?
- Frontend: `undefined% feito` na página. Servidor devolve `percent_done` em `/api/tasks/stats`; conferir o nome que o `app.js` (linha ~88) lê. Depois seguir o checklist "Página" do README (seção 3).
- A linha de ativação da venv do README foi editada para WSL; reverter se for entregar o teste original.

## ONDE PARAMOS (retomar daqui)

- Backend: 10 de 15 testes passam. Próximo alvo sugerido: `find` em `app/storage.py` (resolve `filtrar` e `busca_ignora_maiusculas` juntos). Hipóteses já dadas: linha 33 usa `is` em vez de `==`; linha 15 `id = len(...) + 1` repete id após excluir.
- Perguntas guia: com `status="done"`, qual comparação `find` faz? Bate com o valor que o `toggle` grava? A busca usa `lower()` nos dois lados?
- Frontend: `undefined% feito` ainda aberto.
## Próximo passo ao retomar

1. Rodar `python -m pytest -q` e escolher **uma** falha.
2. Ler o `assert`, achar a regra no README e o código responsável.
3. Corrigir, rodar só esse teste, fazer commit.
4. Quando o backend passar, validar o frontend no navegador e fechar com a explicação exigida na seção 5 do README.
