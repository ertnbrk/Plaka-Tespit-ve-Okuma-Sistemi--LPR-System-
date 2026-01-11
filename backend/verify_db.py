import os
import sys
from sqlalchemy import create_engine, inspect, text
from app.core.config import settings

def check_tables():
    print("--- Database Table Verification ---")
    
    # Force use of local docker settings
    db_url = "postgresql://postgres:password@127.0.0.1:5432/postgres"
    print(f"Connecting to: {db_url}")
    
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)
        
        tables = inspector.get_table_names()
        print(f"\nFound {len(tables)} tables in database 'postgres':")
        for table in tables:
            print(f" - {table}")
            
        if "users" in tables and "complaints" in tables:
            print("\n✅ VERIFICATION SUCCESS: Both 'users' and 'complaints' tables exist.")
            
            # Check row counts
            with engine.connect() as conn:
                user_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
                complaint_count = conn.execute(text("SELECT COUNT(*) FROM complaints")).scalar()
                print(f"   - Users count: {user_count}")
                print(f"   - Complaints count: {complaint_count}")
        else:
            print("\n❌ VERIFICATION FAILED: Tables are missing.")
            print("Running init_db logic now to create them...")
            from app.db.database import Base
            # Import models to register them with Base
            from app.db.models import User, Complaint
            Base.metadata.create_all(bind=engine)
            print("Tables created. Please run this script again to verify.")

    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("Ensure the docker container 'backend-db-1' is running.")

if __name__ == "__main__":
    check_tables()
