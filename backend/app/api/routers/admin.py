from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import crud
from app.api import deps
from app.schemas.users import UserResponse
from app.schemas.complaints import ComplaintResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user)
):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/complaints", response_model=List[ComplaintResponse])
def read_complaints(
    skip: int = 0,
    limit: int = 100,
    plate: Optional[str] = None,
    user_email: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_user)
):
    complaints = crud.get_all_complaints(
        db, skip=skip, limit=limit, 
        plate=plate, user_email=user_email, status=status
    )
    return complaints
