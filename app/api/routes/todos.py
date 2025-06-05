from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_user
from app.domain.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import TodoService

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Todo一覧取得"""
    return TodoService.get_todos(db, current_user.id, skip, limit)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """特定Todo取得"""
    todo = TodoService.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Todo作成"""
    return TodoService.create_todo(db, todo_data, current_user.id)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Todo更新"""
    todo = TodoService.update_todo(db, todo_id, todo_data, current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Todo削除"""
    success = TodoService.delete_todo(db, todo_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
