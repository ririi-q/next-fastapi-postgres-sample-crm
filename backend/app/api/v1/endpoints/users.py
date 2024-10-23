from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=schemas.user.UserInDB)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.user.UserInDB])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.user.UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.user.UserInDB)
def update_user(
    user_id: int,
    user_update: schemas.user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_user = crud.user.get_user_by_email(db, email=user_update.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    updated_user = crud.user.update_user(db, user_id=user_id, user_update=user_update, current_user=current_user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or you don't have permission to update")
    return updated_user

@router.delete("/{user_id}", response_model=schemas.user.UserInDB)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    deleted_user = crud.user.delete_user(db, user_id=user_id, current_user=current_user)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found or you don't have permission to delete")
    return deleted_user
