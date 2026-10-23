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

class DoneTask(BaseModel):
    complete: str

    @field_validator("complete")
    @classmethod
    def validate_comlete(cls, value):
        if value != "true" or value != "false":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Значение должно быть либо true либо  false"
            )
        else:
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
            if i["id"] == task_id:
                return i
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачи с таким ID нет"
        )

@router.post("/tasks", status_code=201)
def add_task(arg: AddTask):
    return database_processing.add(arg.title)

@router.patch("/tasks/{task_id}")
def done_task(task_id: DoneTask):
    result = database_processing.done(task_id.complete)
    if result == 0 or result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет задачи с таким id!"
        )
    if result:
        return result

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    result = database_processing.delete(task_id)
    if result is None or result == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет задачи с таким id!"
        )
    if result:
        return
    