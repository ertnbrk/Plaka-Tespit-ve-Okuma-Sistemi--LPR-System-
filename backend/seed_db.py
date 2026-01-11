import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, engine, Base
from app.db.models import User, Complaint
from app.core.security import get_password_hash
from sqlalchemy.orm import Session

def seed_db():
    print("--- Database Seeding Script ---")
    
    # 1. Reset Schema
    print("Resetting database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Tables dropped and recreated.")

    db = SessionLocal()

    try:
        # 2. Create Users
        print("\nCreating default users...")
        
        # Admin
        admin_pass = get_password_hash("123")
        admin = User(
            email="admin@plaka.gov.tr",
            hashed_password=admin_pass,
            name="Sistem Yöneticisi",
            role="admin",
            is_active=True
        )
        db.add(admin)
        
        # Officer
        officer_pass = get_password_hash("123")
        officer = User(
            email="demo@plaka.gov.tr",
            hashed_password=officer_pass,
            name="Demo Memur",
            role="officer",
            is_active=True
        )
        db.add(officer)
        
        db.commit()
        print("✅ Users created:")
        print("   - Admin: admin@plaka.gov.tr / 123")
        print("   - Officer: demo@plaka.gov.tr / 123")

        # 3. Create Sample Complaints
        print("\nCreating sample complaints...")
        
        # Need to fetch users back to get IDs
        db.refresh(admin)
        db.refresh(officer)

        c1 = Complaint(
            user_id=officer.id,
            plate="34ABC123",
            description="Hatalı park, yaya geçidi ihlali.",
            date="11.01.2026",
            location="İstanbul / Kadıköy / Caferağa - Moda Cd. No:10",
            city="İstanbul",
            district="Kadıköy",
            neighborhood="Caferağa",
            address_detail="Moda Cd. No:10",
            status="İnceleniyor"
        )
        
        c2 = Complaint(
            user_id=officer.id,
            plate="06EFG456",
            description="Kırmızı ışık ihlali.",
            date="10.01.2026",
            location="Ankara / Çankaya / Kızılay - Atatürk Blv.",
            city="Ankara",
            district="Çankaya",
            neighborhood="Kızılay",
            address_detail="Atatürk Blv.",
            status="Onaylandı",
            admin_note="Video kaydı ile teyit edildi."
        )

        db.add(c1)
        db.add(c2)
        db.commit()
        print("✅ Sample complaints created.")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
