import pytest
from fastapi.testclient import TestClient
from server import app

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def fake_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "tasks.json").write_text('[{"id": 1, "title": "Подготовить отчёт для клиента", "complete": false}, {"id": 2, "title": "Разработать REST API", "complete": true}, {"id": 4, "title": "Настроить PostgreSQL", "complete": false}, {"id": 7, "title": "Интегрировать Telegram-бота", "complete": false}, {"id": 12, "title": "Написать автоматические тесты", "complete": true}, {"id": 20, "title": "Настроить Docker и CI/CD", "complete": false}, {"id": 21, "title": "Изучить FastAPI", "complete": false}, {"id": 22, "title": "  PostgreSQL  ", "complete": false}]')
    (tmp_path / "del_id.json").write_text("[3,5,6,8,9,10,11,13,14,15,16,17,18,19]")
    
    yield

def test_get_all_tasks(fake_data, test_client):
    response = test_client.get("/tasks")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) == 8

def test_get_existing_task(fake_data, test_client):
    response = test_client.get("/tasks/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1

def test_get_nonexistent_task(fake_data, test_client):
    response = test_client.get("/tasks/999")
    assert response.status_code == 404

def test_create_task(fake_data, test_client):
    response = test_client.post("/tasks", json={"title": "test_api"})
    result = response.json()
    assert response.status_code == 201
    assert result["title"] == "test_api"

def test_create_invalid_task(fake_data, test_client):
    response = test_client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422

def test_patch_task(fake_data, test_client):
    response = test_client.patch("/tasks/1", json={"complete": True})
    result = test_client.get("/tasks/1")
    data = result.json()
    assert response.status_code == 200
    assert data["complete"] == True

def test_delete_task(fake_data, test_client):
    response = test_client.delete("/tasks/1")
    assert response.status_code == 204
    result = test_client.get("/tasks")
    result = result.json()
    data = [i["id"] for i in result]
    assert 1 not in data

def test_delete_nonexistent_task(fake_data, test_client):
    response = test_client.delete("/tasks/999")
    assert response.status_code == 404

def test_task_lifecycle(fake_data, test_client):
    response = test_client.post("/tasks", json={"title": "test_api"})
    data = response.json()
    assert response.status_code == 201
    response = test_client.get(f"/tasks/{data['id']}")
    data = response.json()
    assert response.status_code == 200
    response = test_client.patch(f"/tasks/{data['id']}", json={"complete": True})
    data = response.json()
    assert response.status_code == 200
    assert data["complete"] == True
    response = test_client.get(f"/tasks/{data['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["complete"] == True
    response = test_client.delete(f"/tasks/{data['id']}")
    assert response.status_code == 204
    response = test_client.get(f"/tasks/{data['id']}")
    assert response.status_code == 404