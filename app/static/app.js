// TaskBoard - frontend simples, sem frameworks.

const PRIORITY_LABEL = { 1: "Baixa", 2: "Média", 3: "Alta" };

const els = {
  form: document.getElementById("new-task"),
  list: document.getElementById("task-list"),
  stats: document.getElementById("stats"),
  error: document.getElementById("error"),
  filter: document.getElementById("filter-status"),
  search: document.getElementById("search"),
  clearDone: document.getElementById("clear-done"),
  report: document.getElementById("report"),
  reportOutput: document.getElementById("report-output"),
};

function showError(message) {
  els.error.textContent = message;
  els.error.hidden = false;
}

function clearError() {
  els.error.hidden = true;
}

async function api(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    let detail = "";
    try {
      detail = JSON.stringify((await res.json()).detail);
    } catch (_) {}
    throw new Error(`Erro ${res.status} em ${options.method || "GET"} ${url} ${detail}`);
  }
  return res.status === 204 ? null : res.json();
}

function renderTask(task) {
  const li = document.createElement("li");
  li.className = "task" + (task.status === "done" ? " done" : "");

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = task.status === "done";
  checkbox.addEventListener("change", () => toggleTask(task.id));

  const title = document.createElement("span");
  title.className = "title";
  title.textContent = `#${task.id} ${task.title}`;
  for (const tag of task.tags) {
    const badge = document.createElement("span");
    badge.className = "tag";
    badge.textContent = tag;
    title.appendChild(badge);
  }

  const prio = document.createElement("span");
  prio.className = "prio";
  prio.textContent = PRIORITY_LABEL[task.priority];

  const del = document.createElement("button");
  del.className = "danger";
  del.textContent = "×";
  del.title = "Excluir";
  del.addEventListener("click", () => deleteTask(task.id));

  li.append(checkbox, title, prio, del);
  return li;
}

async function loadTasks() {
  const params = new URLSearchParams();
  if (els.filter.value) params.set("status", els.filter.value);
  if (els.search.value.trim()) params.set("q", els.search.value.trim());

  try {
    const tasks = await api(`/api/tasks?${params}`);
    els.list.replaceChildren(...tasks.map(renderTask));
    clearError();
  } catch (err) {
    showError(err.message);
  }
  loadStats();
}

async function loadStats() {
  try {
    const data = await api("/api/tasks/stats");
    els.stats.textContent =
      `${data.total} tarefas · ${data.done} concluídas · ${data.pending} pendentes · ${data.percentDone}% feito`;
  } catch (err) {
    els.stats.textContent = "Estatísticas indisponíveis";
    showError(err.message);
  }
}

async function createTask(event) {
  event.preventDefault();
  const form = els.form;
  const tags = form.tags.value
    .split(",")
    .map((t) => t.trim())
    .filter(Boolean);

  try {
    await api("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: form.title.value,
        priority: Number(form.priority.value),
        tags: tags.length ? tags : null,
      }),
    });
    form.title.value = "";
    form.tags.value = "";
    loadTasks();
  } catch (err) {
    showError(err.message);
  }
}

async function toggleTask(id) {
  try {
    await api(`/api/tasks/${id}/toggle`, { method: "PATCH" });
  } catch (err) {
    showError(err.message);
  }
  loadTasks();
}

async function deleteTask(id) {
  try {
    await api(`/api/tasks/${id}`, { method: "DELETE" });
  } catch (err) {
    showError(err.message);
  }
  loadTasks();
}

async function clearDone() {
  try {
    const data = await api("/api/tasks/done", { method: "DELETE" });
    console.log(`${data.removed} tarefas removidas`);
  } catch (err) {
    showError(err.message);
  }
  loadTasks();
}

async function generateReport() {
  els.reportOutput.hidden = false;
  els.reportOutput.textContent = "Gerando relatório…";
  try {
    const data = await api("/api/report");
    els.reportOutput.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    els.reportOutput.textContent = "";
    showError(err.message);
  }
}

els.form.addEventListener("submit", createTask);
els.filter.addEventListener("change", loadTasks);
els.search.addEventListener("input", loadTasks);
els.clearDone.addEventListener("click", clearDone);
els.report.addEventListener("click", generateReport);

loadTasks();
