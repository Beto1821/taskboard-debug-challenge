# Como rodar os testes

Guia rápido do `pytest` neste projeto. Os testes ficam em `tests/test_api.py`.

> **Regra de ouro:** o teste é a fonte da verdade. Quando teste e código discordam, **o código muda**, nunca o teste.

## Antes de tudo

Ative a venv em cada terminal novo (WSL/Linux):

```bash
source .venv/bin/activate
```

O prompt deve mostrar `(.venv)`. No Windows + PowerShell: `.\.venv\Scripts\Activate.ps1`.

## Rodar todos

```bash
python -m pytest -q
```

- `-q` = saída curta (um `.` por teste que passou, `F` por falha).
- Última linha mostra o placar, ex.: `5 failed, 10 passed`.

## Rodar um teste só

Três formas, da mais exata para a mais flexível.

**1. Caminho completo (recomendado, pega exatamente um):**
```bash
python -m pytest -q tests/test_api.py::test_criar_tarefa_retorna_201
```

**2. Pelo nome, com `-k` (pega todo teste cujo nome contém o texto):**
```bash
python -m pytest -q -k test_criar_tarefa_retorna_201
python -m pytest -q -k filtrar        # trecho do nome
python -m pytest -q -k "titulo or tags"   # vários
```

**3. Só os que falharam na última execução:**
```bash
python -m pytest -q --lf
```

## Lista dos testes (um por vez)

Copie o comando do teste que quer atacar.

| Teste | Comando |
|---|---|
| página inicial carrega | `python -m pytest -q -k test_pagina_inicial_carrega` |
| arquivos estáticos servidos | `python -m pytest -q -k test_arquivos_estaticos_sao_servidos` |
| criar tarefa retorna 201 | `python -m pytest -q -k test_criar_tarefa_retorna_201` |
| título em branco rejeitado | `python -m pytest -q -k test_titulo_em_branco_e_rejeitado` |
| título salvo sem espaços extras | `python -m pytest -q -k test_titulo_e_salvo_sem_espacos_extras` |
| tags não vazam entre tarefas | `python -m pytest -q -k test_tags_nao_vazam_entre_tarefas` |
| tags enviadas são mantidas | `python -m pytest -q -k test_tags_enviadas_sao_mantidas` |
| ids únicos após excluir | `python -m pytest -q -k test_ids_continuam_unicos_apos_excluir` |
| buscar inexistente retorna 404 | `python -m pytest -q -k test_buscar_tarefa_inexistente_retorna_404` |
| filtrar por status | `python -m pytest -q -k test_filtrar_por_status` |
| busca ignora maiúsculas | `python -m pytest -q -k test_busca_ignora_maiusculas` |
| stats com quadro vazio | `python -m pytest -q -k test_stats_com_quadro_vazio` |
| stats com tarefas | `python -m pytest -q -k test_stats_com_tarefas` |
| toggle alterna status | `python -m pytest -q -k test_toggle_alterna_status` |
| limpar concluídas remove todas | `python -m pytest -q -k test_limpar_concluidas_remove_todas` |

Ver a lista atual sem rodar nada:
```bash
python -m pytest --collect-only -q
```

## Opções úteis

| Opção | O que faz |
|---|---|
| `-q` | saída curta |
| `-v` | mostra o nome de cada teste e `PASSED`/`FAILED` |
| `-s` | deixa `print()` aparecer (pytest esconde por padrão) |
| `-x` | para no primeiro teste que falhar |
| `--lf` | roda só os que falharam na última vez |
| `-k texto` | roda testes cujo nome contém `texto` |
| `--tb=short` | traceback mais curto |

Combinar: `python -m pytest -q -s -x -k filtrar`

## Como ler a saída de uma falha

1. Ignore a seção `warnings summary` (o aviso `httpx2` é ruído).
2. Procure a linha que começa com `>`: é a linha do teste que falhou.
3. Leia as linhas `E` logo abaixo: dizem o que veio e o que era esperado.
   Em `assert A == B`, `A` é o que o código devolveu e `B` o que o teste esperava.
4. Com traceback: leia de baixo para cima e ache o último frame dentro de `app/`.
5. Sem traceback (só `assert`): siga o dado. Teste, rota em `main.py`, função ou tipo que ela usa, arquivo onde está definido. Atalho: `grep -rn "nome" app/`.

## Fluxo para cada bug

1. Rodar `python -m pytest -q` e escolher **uma** falha.
2. Ler o `assert` e achar a regra no README (seção 3).
3. Achar o código responsável e corrigir.
4. Rodar **só esse teste**, depois o placar completo (nenhum teste que passava pode quebrar).
5. Commit pequeno: `git add <arquivos>` e `git commit -m "fix: ..."`. Não incluir `tests/`.

## Problemas comuns

- **`source: no such file or directory`**: terminal fora da pasta do projeto. `cd` para a raiz e rode `source .venv/bin/activate`.
- **Mudei o código e nada mudou**: salve o arquivo (Ctrl+S). Se for o servidor (`uvicorn`) sem `--reload`, reinicie.
- **Editei um teste sem querer**: `git restore tests/test_api.py`.
- **`print` não aparece**: use `-s`.
