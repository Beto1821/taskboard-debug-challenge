# Desafio: TaskBoard quebrado 🐛

> Simulado de teste técnico no estilo "suba a aplicação e debugue", parecido com os
> *take-homes* da Mercor e de outras empresas para vagas de Python júnior/pleno.

## Contexto

Você acabou de entrar no time. O dev anterior saiu e deixou o **TaskBoard**, um quadro de
tarefas com uma API em **FastAPI** e uma página web simples. Ele jurou que estava "quase
pronto", mas:

- o servidor nem sobe;
- quando sobe, a página carrega vazia e cheia de erros;
- os usuários reclamam de tarefas com tags estranhas, IDs repetidos e de o sistema
  "travar inteiro" às vezes.

**Sua missão:** colocar a aplicação no ar, achar e corrigir os bugs, e explicar o que fez.

| | |
|---|---|
| ⏱️ **Tempo sugerido** | 90 minutos (cronometre!) |
| 🐞 **Bugs plantados** | **16**: no setup, no backend (Python) e no frontend (JavaScript) |
| ✅ **Pronto quando** | `pytest` todo verde **e** a página funcionando no navegador conforme a especificação abaixo |

---

## 1. Preparando o ambiente (VS Code)

### Pré-requisitos
- **Python 3.10 ou mais novo**: baixe em <https://www.python.org/downloads/> e, na
  instalação, marque **"Add python.exe to PATH"**.
- **VS Code** com a extensão **Python** (da Microsoft), que já traz o debugger (*debugpy*).

### Passo a passo
Abra esta pasta no VS Code (**File → Open Folder**) e, no terminal integrado (`Ctrl + '`):

```powershell
python -m venv .venv
```

```powershell
source .venv/bin/activate
```

```powershell
pip install -r requirements.txt
```

> Se o PowerShell bloquear o `Activate.ps1`, rode antes:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Depois: `Ctrl + Shift + P` → **Python: Select Interpreter** → escolha o `.venv`.

### Subindo o servidor
Há duas formas:

**Pelo terminal** (recarrega sozinho quando você salva um arquivo):
```powershell
uvicorn app.main:app --reload
```

**Pelo debugger do VS Code** (permite usar breakpoints): aba **Run and Debug**
(`Ctrl + Shift + D`) → **"TaskBoard: uvicorn (debug)"** → **F5**.
Nesse modo não há auto-reload: depois de editar, reinicie com `Ctrl + Shift + F5`.

Com o servidor no ar:
- Página: <http://127.0.0.1:8000>
- Documentação interativa da API (Swagger): <http://127.0.0.1:8000/docs>

### Rodando os testes
```powershell
pytest -v
```
Ou pela aba **Testing** (ícone de frasco) do VS Code. Também existe a configuração
**"TaskBoard: pytest (debug)"** para parar em breakpoints durante os testes.

---

## 2. Estrutura do projeto

```
app/
  main.py          # rotas da API (FastAPI)
  models.py        # modelos Pydantic v2
  storage.py       # "banco" em memória
  static/
    index.html     # página
    app.js         # lógica do frontend
    style.css
tests/
  test_api.py      # testes de aceitação (NÃO edite)
.vscode/           # configurações de debug e testes
gabarito/          # ⚠️ spoiler: só abra no final
```

---

## 3. Especificação (como o sistema DEVE funcionar)

### API

| Método | Rota | Comportamento esperado |
|---|---|---|
| `GET` | `/` | Devolve a página `index.html`. |
| `GET` | `/static/...` | Serve os arquivos de `app/static/`. |
| `GET` | `/api/tasks` | Lista as tarefas. Filtros opcionais: `?status=pending` ou `?status=done`, e `?q=texto` (busca no título **sem diferenciar maiúsculas de minúsculas**). |
| `POST` | `/api/tasks` | Cria uma tarefa. Responde **201**. Título obrigatório e não pode ser só espaços (**422**); espaços nas pontas são removidos. Prioridade de 1 a 3 (padrão 2). |
| `GET` | `/api/tasks/{id}` | Devolve a tarefa, ou **404** se ela não existir. |
| `GET` | `/api/tasks/stats` | `{total, done, pending, percent_done}`. Com o quadro vazio, `percent_done` é `0.0`. |
| `PATCH` | `/api/tasks/{id}/toggle` | Alterna entre `pending` e `done`. **404** se não existir. |
| `DELETE` | `/api/tasks/{id}` | Remove a tarefa. Responde **204**, ou **404** se não existir. |
| `DELETE` | `/api/tasks/done` | Remove **todas** as tarefas concluídas e devolve `{"removed": n}`. |
| `GET` | `/api/report` | Gera um relatório (simula um processamento de ~3 s). **Enquanto ele roda, o resto da aplicação precisa continuar respondendo normalmente.** |

### Regras de negócio
- Toda tarefa recebe automaticamente a tag `prio-N` (N = prioridade), **somada** às tags
  que o usuário enviou. Exemplo: `["urgente"]` com prioridade 3 vira `["urgente", "prio-3"]`.
  Sem tags enviadas, fica só `["prio-N"]`. As tags de uma tarefa nunca podem aparecer em outra.
- **IDs são únicos** e nunca são reaproveitados, nem depois de excluir tarefas.

### Página (teste manual no navegador)
- [ ] A lista de tarefas aparece ao abrir a página, sem mensagem de erro.
- [ ] Adicionar uma tarefa faz ela aparecer na lista na hora.
- [ ] A linha de estatísticas mostra os números certos, inclusive o **% feito**.
- [ ] Marcar o checkbox risca a tarefa e atualiza as estatísticas.
- [ ] Filtro (Todas / Pendentes / Concluídas) e busca funcionam.
- [ ] Botão × exclui a tarefa.
- [ ] "Limpar concluídas" remove todas as concluídas.
- [ ] Clicar em "Gerar relatório" e, **durante** os 3 segundos, adicionar uma tarefa em
      outra aba: a outra aba precisa responder na hora, sem ficar presa.

> 💡 Para depurar o frontend, use o **DevTools** do navegador (`F12`): a aba **Console**
> mostra erros de JavaScript e a aba **Network** mostra cada requisição, com URL,
> método e status code.

---

## 4. Regras
1. **Não edite `tests/test_api.py`.** Corrija o código da aplicação.
2. Corrija a causa do problema, não o sintoma. Por exemplo, nada de `try/except` engolindo
   o erro para o teste passar.
3. Mudanças pequenas e cirúrgicas: não reescreva o projeto do zero.
4. Pode consultar documentação oficial (FastAPI, Pydantic, Python, MDN).

## 5. Entrega
Crie um arquivo **`NOTAS.md`** na raiz com uma linha por bug:

| # | Sintoma | Causa | Correção | Como descobri |
|---|---|---|---|---|
| 1 | Servidor não sobe: `ImportError ...` | ... | ... | traceback no terminal |

Isso é tão importante quanto o código: em testes reais (inclusive na Mercor), costuma vir
depois uma conversa em que você **explica e defende** cada correção.

## 6. Critérios de avaliação

| Critério | Peso |
|---|---|
| Aplicação sobe e a página funciona de ponta a ponta | ⭐⭐⭐ |
| Testes passando (`pytest`) | ⭐⭐⭐ |
| Qualidade das correções (causa raiz, código limpo) | ⭐⭐ |
| `NOTAS.md` claro, explicando o raciocínio | ⭐⭐ |
| Processo: ler o traceback, isolar o problema, um bug por vez | ⭐ |

---

## 7. Dicas (abra só se travar)

<details>
<summary>Dica geral de método</summary>

1. Leia o **traceback de baixo para cima**: a última linha é o erro, e as linhas acima
   mostram onde ele aconteceu.
2. Primeiro faça o servidor **subir**. Depois deixe a **página** funcionando. Por último,
   cuide da **lógica**.
3. Rode `pytest -v` e ataque **um teste vermelho por vez**.
4. Use o `/docs` para chamar a API direto, sem o frontend no meio. Assim você descobre se
   o bug está no backend ou no JavaScript.
5. Breakpoint no VS Code: clique à esquerda do número da linha, suba com F5 e faça a
   requisição. Use F10 (próxima linha) e F11 (entrar na função).
</details>

<details>
<summary>Nível 1: o servidor não sobe (2 bugs)</summary>

- Leia a mensagem de erro com atenção: ela diz **qual nome** não foi encontrado e **onde**.
- Depois de corrigir o primeiro, aparece outro erro, agora sobre um **diretório**.
</details>

<details>
<summary>Nível 2: a página carrega, mas quebrada (4 bugs)</summary>

- Abra o DevTools → **Network** e veja quais requisições ficam vermelhas e com qual status.
- `404` quer dizer URL errada. `405` quer dizer **método HTTP** errado.
- `422` numa rota que nem recebe parâmetro? Pense em **qual rota o FastAPI escolheu**.
  A ordem de declaração importa.
- Um valor aparecendo como `undefined` no JS geralmente é nome de campo diferente entre
  o backend e o frontend.
</details>

<details>
<summary>Nível 3: lógica e regras de negócio (9 bugs)</summary>

- Um erro **500** com o quadro vazio: e se o total for zero?
- Criar uma função que *valida*, mas não *impede* nada.
- Tags vazando entre tarefas: pesquise "Python mutable default argument".
- IDs repetidos: como o ID é calculado? O que acontece depois de um `delete`?
- Rota que devolve `200` com um "erro" dentro, ou `500`: como o FastAPI devolve 404?
- Status code de criação: veja o parâmetro `status_code` do decorator.
- Filtro que nunca encontra nada: `is` e `==` não são a mesma coisa.
- "Limpar concluídas" deixa sobrar algumas: o que acontece ao remover itens de uma lista
  **enquanto você percorre essa mesma lista**?
- E a busca diferencia maiúsculas de minúsculas?
</details>

<details>
<summary>Nível 4: concorrência (1 bug, sem teste automático)</summary>

- O relatório "trava o servidor inteiro". Pesquise "FastAPI async def time.sleep blocking
  event loop". Há duas correções válidas. Qual você escolheria, e por quê?
</details>

---

## 8. Depois de terminar
- Compare com [`gabarito/SOLUCAO.md`](gabarito/SOLUCAO.md).
- Desafio extra (pleno): troque o armazenamento em memória por **SQLite** e adicione um
  teste que prove que o `/api/report` não bloqueia outras requisições.
