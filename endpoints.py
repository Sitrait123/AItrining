from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator
import database_processing

router = APIRouter()

class AddTask(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Название задачи не может быть пустым")

        return value

@router.get("/tasks")
def do_list():
    resullt = database_processing.list_for_api()
    if resullt:
        return resullt
    else:
        return []

@router.get("/tasks/{task_id}")
def execute_list_by_ID(task_id: int):
    result = database_processing.list_for_api()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет задач!"
        )
    else:
        for i in result:
            try:      
                if i["id"] == task_id:
                    return i
            except:
                pass
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачи с таким ID нет"
        )

@router.post("/tasks", status_code=201)
def add_task(arg: AddTask):
    return database_processing.add(arg.title)