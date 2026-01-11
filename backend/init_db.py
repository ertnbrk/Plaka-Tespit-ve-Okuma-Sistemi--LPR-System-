import os
import sys
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

try:
    from app.core.config import settings
    from app.db.database import engine, Base
    from app.db.models import User, Complaint
except ImportError as e:
    print(f"Import Error: {e}")
    sys.path.append(os.getcwd())
    from app.core.config import settings
    from app.db.database import engine, Base
    from app.db.models import User, Complaint

def init_db():
    print("--- Database Initialization Script ---")
    
    # Force local connection if .env blocked
    db_url = settings.DATABASE_URL
    if not db_url or "supabase" in db_url:
        print("Using fallback local URL...")
        db_url = "postgresql://postgres:password@127.0.0.1:5432/postgres"
    
    # Mask password for display
    if "@" in db_url:
        start, rest = db_url.split("@")
        user_part = start.split("//")[1]
        host_part = rest
        print(f"Target Database: postgresql://{user_part.split(':')[0]}:****@{host_part}")
    else:
        print(f"Target Database: {db_url}")

    print("\nAttempting to connect and create tables...")
    
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)
        print("✅ Success! Tables 'users' and 'complaints' should now exist.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
