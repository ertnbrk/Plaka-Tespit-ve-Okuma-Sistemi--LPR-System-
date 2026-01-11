import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine, Base
from app.db.models import User
from app.core.security import get_password_hash
from app.schemas.users import UserCreate
from app.db import crud

def create_admin():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print("--- Create Admin User ---")
    email = input("Email: ").strip()
    if not email:
        print("Email is required.")
        return
        
    # Check if exists
    existing = crud.get_user_by_email(db, email)
    if existing:
        print(f"User {email} already exists.")
        make_admin = input("Do you want to promote this user to admin? (y/n): ")
        if make_admin.lower() == 'y':
            existing.role = "admin"
            db.commit()
            print("User promoted to admin.")
        return

    password = input("Password: ").strip()
    if not password:
        print("Password is required.")
        return

    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return

    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        name=name,
        role="admin",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    print(f"Admin user {email} created successfully.")
    db.close()

if __name__ == "__main__":
    create_admin()
