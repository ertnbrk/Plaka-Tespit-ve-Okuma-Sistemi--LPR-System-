import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print("\n--- APP DATABASE USERS ---")
        print(f"{'ID':<5} {'NAME':<20} {'EMAIL':<30} {'ROLE':<10}")
        print("-" * 70)
        for u in users:
            print(f"{u.id:<5} {u.name:<20} {u.email:<30} {u.role:<10}")
        print("-" * 70)
        print(f"Total: {len(users)}\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
