from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.models.todo import Todo
from app.domain.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    @staticmethod
    def get_todos(db: Session, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Todo]:
        return db.query(Todo).filter(
            Todo.user_id == user_id,
            Todo.is_deleted == False
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_todo(db: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        return db.query(Todo).filter(
            Todo.id == todo_id,
            Todo.user_id == user_id,
            Todo.is_deleted == False
        ).first()

    @staticmethod
    def create_todo(db: Session, todo_data: TodoCreate, user_id: UUID) -> Todo:
        db_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            user_id=user_id
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def update_todo(db: Session, todo_id: UUID, todo_data: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        db_todo = TodoService.get_todo(db, todo_id, user_id)
        if not db_todo:
            return None
        
        update_data = todo_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(db: Session, todo_id: UUID, user_id: UUID) -> bool:
        db_todo = TodoService.get_todo(db, todo_id, user_id)
        if not db_todo:
            return False
        
        db_todo.is_deleted = True
        db.commit()
        return True
