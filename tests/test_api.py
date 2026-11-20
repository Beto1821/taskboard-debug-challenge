"""Testes de aceitação do TaskBoard.

Eles descrevem o comportamento ESPERADO (ver README). No começo quase
todos falham — a meta é deixar todos verdes sem alterar este arquivo.

Rodar:  pytest -v
"""

import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.storage import TaskStore


@pytest.fixture
def client(monkeypatch):
    # Cada teste começa com um quadro vazio.
    monkeypatch.setattr(main, "store", TaskStore())
    return TestClient(main.app)


def create(client, title="Estudar FastAPI", priority=2, tags=None):
    body = {"title": title, "priority": priority}
    if tags is not None:
        body["tags"] = tags
    return client.post("/api/tasks", json=body)


# --- Página -----------------------------------------------------------------

def test_pagina_inicial_carrega(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "TaskBoard" in res.text


def test_arquivos_estaticos_sao_servidos(client):
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/style.css").status_code == 200


# --- Criação ----------------------------------------------------------------

def test_criar_tarefa_retorna_201(client):
    res = create(client)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Estudar FastAPI"
    assert data["status"] == "pending"
    assert data["tags"] == ["prio-2"]


def test_titulo_em_branco_e_rejeitado(client):
    res = create(client, title="   ")
    assert res.status_code == 422


def test_titulo_e_salvo_sem_espacos_extras(client):
    res = create(client, title="  Ler docs  ")
    assert res.json()["title"] == "Ler docs"


def test_tags_nao_vazam_entre_tarefas(client):
    a = create(client, priority=1).json()
    b = create(client, priority=3).json()
    assert a["tags"] == ["prio-1"]
    assert b["tags"] == ["prio-3"]
    # E a primeira continua igual depois de criar a segunda:
    assert client.get(f"/api/tasks/{a['id']}").json()["tags"] == ["prio-1"]


def test_tags_enviadas_sao_mantidas(client):
    res = create(client, priority=3, tags=["urgente"])
    assert res.json()["tags"] == ["urgente", "prio-3"]


def test_ids_continuam_unicos_apos_excluir(client):
    ids = [create(client, title=f"T{i}").json()["id"] for i in range(3)]
    assert client.delete(f"/api/tasks/{ids[0]}").status_code == 204
    novo = create(client, title="Nova").json()
    restantes = [t["id"] for t in client.get("/api/tasks").json()]
    assert len(restantes) == len(set(restantes)), f"IDs repetidos: {restantes}"
    assert novo["id"] not in ids


# --- Leitura ----------------------------------------------------------------

def test_buscar_tarefa_inexistente_retorna_404(client):
    res = client.get("/api/tasks/999")
    assert res.status_code == 404


def test_filtrar_por_status(client):
    a = create(client, title="A").json()
    create(client, title="B")
    client.patch(f"/api/tasks/{a['id']}/toggle")

    done = client.get("/api/tasks", params={"status": "done"}).json()
    pending = client.get("/api/tasks", params={"status": "pending"}).json()
    assert [t["title"] for t in done] == ["A"]
    assert [t["title"] for t in pending] == ["B"]


def test_busca_ignora_maiusculas(client):
    create(client, title="Revisar Pull Request")
    create(client, title="Lavar louça")
    res = client.get("/api/tasks", params={"q": "pull"}).json()
    assert [t["title"] for t in res] == ["Revisar Pull Request"]


# --- Estatísticas -------------------------------------------------------------

def test_stats_com_quadro_vazio(client):
    res = client.get("/api/tasks/stats")
    assert res.status_code == 200
    assert res.json() == {"total": 0, "done": 0, "pending": 0, "percent_done": 0.0}


def test_stats_com_tarefas(client):
    ids = [create(client, title=f"T{i}").json()["id"] for i in range(4)]
    client.patch(f"/api/tasks/{ids[0]}/toggle")
    res = client.get("/api/tasks/stats")
    assert res.status_code == 200
    assert res.json() == {"total": 4, "done": 1, "pending": 3, "percent_done": 25.0}


# --- Atualização e remoção ------------------------------------------------------

def test_toggle_alterna_status(client):
    t = create(client).json()
    assert client.patch(f"/api/tasks/{t['id']}/toggle").json()["status"] == "done"
    assert client.patch(f"/api/tasks/{t['id']}/toggle").json()["status"] == "pending"


def test_limpar_concluidas_remove_todas(client):
    ids = [create(client, title=f"T{i}").json()["id"] for i in range(5)]
    for task_id in ids[:4]:  # 4 concluídas seguidas, 1 pendente
        client.patch(f"/api/tasks/{task_id}/toggle")

    res = client.delete("/api/tasks/done")
    assert res.json() == {"removed": 4}
    assert [t["id"] for t in client.get("/api/tasks").json()] == [ids[4]]
