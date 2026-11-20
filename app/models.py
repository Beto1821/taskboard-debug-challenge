"""Modelos de entrada e saída da API (Pydantic v2)."""

from pydantic import BaseModel, Field, field_validator


class TaskIn(BaseModel):
    """Corpo da requisição para criar uma tarefa."""

    title: str
    priority: int = Field(default=2, ge=1, le=3)
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        if not value.strip():
            ValueError("O título não pode ficar em branco")
        return value.strip()


class Task(BaseModel):
    """Tarefa como é devolvida pela API."""

    id: int
    title: str
    priority: int
    tags: list[str]
    status: str  # "pending" ou "done"


class Stats(BaseModel):
    """Resumo do quadro de tarefas."""

    total: int
    done: int
    pending: int
    percent_done: float
