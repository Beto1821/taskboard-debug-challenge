"""TaskBoard: API de tarefas + página web.

Para rodar (a partir da pasta raiz do projeto):
    uvicorn app.main:app --reload
"""

import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import Stats, Task, TaskCreate
from app.storage import TaskStore

BASE_DIR = Path(__file__).parent

app = FastAPI(title="TaskBoard")
app.mount("/static", StaticFiles(directory=BASE_DIR / "statics"), name="static")

store = TaskStore()


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/tasks", response_model=list[Task])
def list_tasks(status: str | None = None, q: str | None = None):
    """Lista tarefas. Filtros opcionais: ?status=pending|done e ?q=texto."""
    return store.find(status=status, q=q)


@app.post("/api/tasks", response_model=Task)
def create_task(payload: TaskCreate):
    return store.add(**payload.model_dump(exclude_none=True))


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = store.get(task_id)
    if task is None:
        return {"error": "Tarefa não encontrada"}
    return task


@app.get("/api/tasks/stats", response_model=Stats)
def get_stats():
    return store.stats()


@app.patch("/api/tasks/{task_id}/toggle", response_model=Task)
def toggle_task(task_id: int):
    task = store.toggle(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


@app.delete("/api/tasks/done")
def clear_done():
    """Remove todas as tarefas concluídas."""
    return {"removed": store.clear_done()}


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not store.delete(task_id):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.get("/api/report")
async def report():
    """Gera um relatório 'pesado' (simulado com uma espera de 3 segundos)."""
    time.sleep(3)
    return {"generated_at": datetime.now().isoformat(timespec="seconds"), **store.stats()}
