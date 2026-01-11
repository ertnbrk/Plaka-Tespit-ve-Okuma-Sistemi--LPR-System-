#!/usr/bin/env python3
"""
Database Migration Script
Drops existing tables and recreates them with the new schema
"""

import sys
import os
from dotenv import load_dotenv

# Force reload of .env
load_dotenv(override=True)

try:
    from app.core.config import settings
    from app.db.database import engine, Base
    from app.db.models import User, Complaint
    from sqlalchemy import text
except ImportError as e:
    print(f"Import Error: {e}")
    sys.path.append(os.getcwd())
    from app.core.config import settings
    from app.db.database import engine, Base
    from app.db.models import User, Complaint
    from sqlalchemy import text

def migrate_db():
    print("--- Database Migration Script ---")
    print("⚠️  WARNING: This will DROP all existing tables and recreate them!")
    print("⚠️  All data will be LOST!")

    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() != "yes":
        print("Migration cancelled.")
        return

    db_url = settings.DATABASE_URL

    # Mask password for display
    if "@" in db_url:
        start, rest = db_url.split("@")
        user_part = start.split("//")[1]
        host_part = rest
        print(f"\nTarget Database: postgresql://{user_part.split(':')[0]}:****@{host_part}")
    else:
        print(f"\nTarget Database: {db_url}")

    print("\n1. Dropping all existing tables...")

    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("   ✅ All tables dropped successfully")
    except Exception as e:
        print(f"   ⚠️  Error dropping tables: {e}")

    print("\n2. Creating new tables with updated schema...")

    try:
        # Create all tables with new schema
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tables created successfully")

        # Verify tables
        with engine.connect() as conn:
            result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
            tables = [row[0] for row in result]
            print(f"\n   Created tables: {', '.join(tables)}")

    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        return

    print("\n✅ Migration completed successfully!")
    print("\nNew schema changes:")
    print("  - User model: 'full_name' → 'name', 'is_admin' → 'role'")
    print("  - Complaint model: Added location fields (city, district, neighborhood, address_detail)")
    print("  - Complaint model: 'incident_datetime' → 'date' (string format)")
    print("  - Complaint model: Status now uses Turkish values (İnceleniyor, Onaylandı, Reddedildi)")
    print("  - Complaint model: Added 'admin_note' field")

    print("\n⚠️  Note: You need to recreate admin users and test data.")
    print("   Run: python create_admin.py")

if __name__ == "__main__":
    migrate_db()
