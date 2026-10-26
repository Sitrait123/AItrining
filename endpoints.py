from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator, StrictBool
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

    
class PatchTask(BaseModel):
    complete: StrictBool


    
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
def done_undone_task(task_id: int, arg: PatchTask):
    if arg.complete == True:
        result = database_processing.done(task_id)
        if result == 0 or result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет задачи с таким id!"
            )
        if result:
            return result
    elif arg.complete == False:
        result = database_processing.undone(task_id)
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
    