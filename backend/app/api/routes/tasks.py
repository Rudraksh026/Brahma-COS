from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.repositories.task_repository import create_task,get_all_tasks,get_task,approve_task,reject_task
router=APIRouter(prefix="/tasks",tags=["Tasks"])
@router.post("/",response_model=TaskResponse)
def add_task(task:TaskCreate,db:Session=Depends(get_db)): return create_task(db,task)
@router.get("/",response_model=list[TaskResponse])
def read_tasks(db:Session=Depends(get_db)): return get_all_tasks(db)
@router.get("/{task_id}",response_model=TaskResponse)
def read_task(task_id:int,db:Session=Depends(get_db)):
    task=get_task(db,task_id)
    if not task: raise HTTPException(404,"Task not found")
    return task
@router.post("/{task_id}/approve",response_model=TaskResponse)
def approve(task_id:int,db:Session=Depends(get_db)):
    task=approve_task(db,task_id)
    if not task: raise HTTPException(404,"Task not found")
    return task
@router.post("/{task_id}/reject",response_model=TaskResponse)
def reject(task_id:int,db:Session=Depends(get_db)):
    task=reject_task(db,task_id)
    if not task: raise HTTPException(404,"Task not found")
    return task
