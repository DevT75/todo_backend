from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from models import TodoModel, UserModel
from schemas import TodoCreateSchema, TodoUpdateSchema, TodoResponseSchema
from crud import create_todo, get_todo_by_id, get_all_todos, update_todo, delete_todo
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TodoResponseSchema)
async def create(todo: TodoCreateSchema, current_user: UserModel = Depends(get_current_user)):
    todo_model = TodoModel(**todo.dict())
    result = await create_todo(todo_model)
    return result

@router.get("/{id}", response_model=TodoResponseSchema)
async def read(id: str, current_user: UserModel = Depends(get_current_user)):
    todo = await get_todo_by_id(id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/", response_model=List[TodoResponseSchema])
async def read_all(current_user: UserModel = Depends(get_current_user)):
    todos = await get_all_todos()
    return todos

@router.put("/{id}", response_model=TodoResponseSchema)
async def update(id: str, todo: TodoUpdateSchema, current_user: UserModel = Depends(get_current_user)):
    updated_todo = await update_todo(id, todo.dict(exclude_unset=True))
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{id}")
async def delete(id: str, current_user: UserModel = Depends(get_current_user)):
    await delete_todo(id)
    return {"detail": "Todo deleted"}
