import json
import database_processing

def test_add_first_task(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    database_processing.add("Тест на id 1")

    test_tasks = tmp_path / "tasks.json"
    with open(test_tasks, "r") as file:
        result = json.load(file)
    assert result[0]["id"] == 1

def test_add_after_delete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    database_processing.add("Тест на удаление")
    database_processing.delete(1)
    database_processing.add("Ещё тест")

    test_tasks = tmp_path / "tasks.json"
    with open(test_tasks, "r") as file:
        result = json.load(file)
    assert result[0]["id"] != 1

def test_delete_nonexistent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    database_processing.add("Тест")
    result = database_processing.delete(999)
    assert result == 0

def test_empty_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    test_tasks = tmp_path / "tasks.json"
    test_tasks.write_text(json.dumps([]))

    result = database_processing.list()
    assert result == 0