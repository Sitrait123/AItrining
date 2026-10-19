from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import database_processing

router = APIRouter()

class AddTask(BaseModel):
    title: str


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
        return []
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

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(arg: AddTask):
    if len(arg.title.strip()) > 0:
        result = database_processing.add(arg.title)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Название задачи не может быть пустым"
        )