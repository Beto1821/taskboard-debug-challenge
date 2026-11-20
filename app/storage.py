"""Armazenamento em memória das tarefas.

Não há banco de dados: tudo some quando o servidor reinicia.
"""


class TaskStore:
    def __init__(self) -> None:
        self._tasks: list[dict] = []

    def add(self, title: str, priority: int = 2, tags=[]) -> dict:
        # Toda tarefa ganha automaticamente uma tag com a prioridade.
        tags.append(f"prio-{priority}")
        task = {
            "id": len(self._tasks) + 1,
            "title": title,
            "priority": priority,
            "tags": tags,
            "status": "pending",
        }
        self._tasks.append(task)
        return task

    def get(self, task_id: int) -> dict | None:
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        return None

    def find(self, status: str | None = None, q: str | None = None) -> list[dict]:
        result = self._tasks
        if status:
            result = [t for t in result if t["status"] is status]
        if q:
            result = [t for t in result if q in t["title"]]
        return result

    def toggle(self, task_id: int) -> dict | None:
        task = self.get(task_id)
        if task is None:
            return None
        task["status"] = "done" if task["status"] == "pending" else "pending"
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def clear_done(self) -> int:
        removed = 0
        for task in self._tasks:
            if task["status"] == "done":
                self._tasks.remove(task)
                removed += 1
        return removed

    def stats(self) -> dict:
        total = len(self._tasks)
        done = sum(1 for t in self._tasks if t["status"] == "done")
        return {
            "total": total,
            "done": done,
            "pending": total - done,
            "percent_done": round(done / total * 100, 1),
        }
