from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud
from app.api import deps
from app.core import security
from app.schemas.users import UserCreate, UserResponse
from app.schemas.auth import Token
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=201)
def register(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    try:
        user = crud.get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )
        user = crud.create_user(db, user=user_in)
        return {"success": True, "message": "Kayıt başarılı"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"REGISTER ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_email(db, email=login_data.email)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = security.create_access_token(data={"sub": user.email})

    # Return token with user object as expected by frontend
    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(deps.get_current_active_user)):
    return current_user
