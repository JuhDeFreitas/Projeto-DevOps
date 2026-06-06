# =========================
# TESTE 1 - HOME ROUTE
# =========================
def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Task Manager API"}


# =========================
# TESTE 2 - CREATE SEM CONTENT-TYPE
# =========================
def test_create_task_rejects_missing_content_type(client):
    response = client.post("/tasks", data="{}")

    assert response.status_code == 415


# =========================
# TESTE 3 - TITLE OBRIGATÓRIO
# =========================
def test_create_task_requires_title(client):
    response = client.post("/tasks", json={"description": "Descrição"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Campo title obrigatório"


# =========================
# TESTE 4 - CREATE + RETRIEVE
# =========================
def test_create_task_and_retrieve_it(client):
    payload = {"title": "Estudar", "description": "Revisar Flask"}
    created = client.post("/tasks", json=payload)

    assert created.status_code == 201

    data = created.get_json()
    assert data["title"] == "Estudar"
    assert data["description"] == "Revisar Flask"
    assert data["status"] == "pending"

    task_id = data["id"]
    retrieved = client.get(f"/tasks/{task_id}")

    assert retrieved.status_code == 200
    assert retrieved.get_json()["id"] == task_id


# =========================
# TESTE 5 - LISTAR TASKS
# =========================
def test_get_tasks_returns_all_tasks(client):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})

    response = client.get("/tasks")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Tarefa 1"
    assert data[1]["title"] == "Tarefa 2"


# =========================
# TESTE 6 - TASK NÃO EXISTE
# =========================
def test_get_task_not_found_returns_404(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Task não encontrada"


# =========================
# TESTE 7 - UPDATE TASK
# =========================
def test_update_task(client):
    created = client.post("/tasks", json={"title": "Original"})
    task_id = created.get_json()["id"]

    updated = client.put(
        f"/tasks/{task_id}",
        json={"title": "Atualizada", "status": "done"}
    )

    assert updated.status_code == 200

    data = updated.get_json()
    assert data["title"] == "Atualizada"
    assert data["status"] == "done"


# =========================
# TESTE 8 - UPDATE NOT FOUND
# =========================
def test_update_task_not_found_returns_404(client):
    response = client.put("/tasks/999", json={"title": "Nada"})

    assert response.status_code == 404


# =========================
# TESTE 9 - DELETE TASK
# =========================
def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Deletar"})
    task_id = created.get_json()["id"]

    deleted = client.delete(f"/tasks/{task_id}")

    assert deleted.status_code == 200
    assert deleted.get_json()["message"] == "Task removida com sucesso"

    missing = client.get(f"/tasks/{task_id}")
    assert missing.status_code == 404


# =========================
# TESTE 10 - PATCH STATUS
# =========================
def test_update_task_status_only(client):
    created = client.post("/tasks", json={"title": "Status teste"})
    task_id = created.get_json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "in_progress"