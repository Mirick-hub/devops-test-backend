"""
Тести для базового CRUD задач.

Тут перевіряється лише той функціонал, що вже реалізований у базовому проєкті.
Тести для фільтрації, нового endpoint'у та бізнес-правила статусу потрібно дописати
самостійно разом із відповідною реалізацією (Завдання 1-3).
"""


def _create_task(client, **overrides):
    payload = {"title": "Buy milk", "description": "2 liters"} | overrides
    return client.post("/tasks", json=payload)


def test_create_task_returns_201_with_default_status(client):
    response = _create_task(client)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["status"] == "todo"
    assert body["priority"] == "medium"


def test_create_task_rejects_empty_title(client):
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


def test_list_tasks_returns_all_created_tasks(client):
    _create_task(client, title="First task")
    _create_task(client, title="Second task")

    response = client.get("/tasks")

    assert response.status_code == 200
    titles = [task["title"] for task in response.json()]
    assert titles == ["First task", "Second task"]


def test_get_task_by_id(client):
    created = _create_task(client).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_returns_404_for_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404


def test_update_task_changes_only_provided_fields(client):
    created = _create_task(client).json()

    response = client.patch(f"/tasks/{created['id']}", json={"status": "in_progress"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["title"] == created["title"]


def test_update_task_returns_404_for_missing_task(client):
    response = client.patch("/tasks/999", json={"status": "done"})

    assert response.status_code == 404


def test_delete_task_removes_it(client):
    created = _create_task(client).json()

    delete_response = client.delete(f"/tasks/{created['id']}")
    get_response = client.get(f"/tasks/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_delete_task_returns_404_for_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
