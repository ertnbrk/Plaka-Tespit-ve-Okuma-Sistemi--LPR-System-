from sqlalchemy.orm import Session
from app.db.models import User, Complaint
from app.schemas.users import UserCreate
from app.schemas.complaints import ComplaintCreate
from app.core.security import get_password_hash
from app.services.plate_service import clean_and_validate_plate

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_complaint(db: Session, complaint: ComplaintCreate, user_id: int):
    # Clean plate
    cleaned_plate = clean_and_validate_plate(complaint.plate)

    db_complaint = Complaint(
        plate=cleaned_plate,
        description=complaint.description,
        date=complaint.date,
        location=complaint.location,
        city=complaint.city,
        district=complaint.district,
        neighborhood=complaint.neighborhood,
        address_detail=complaint.address_detail,
        user_id=user_id
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def get_complaints_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Complaint).filter(Complaint.user_id == user_id)\
             .order_by(Complaint.created_at.desc())\
             .offset(skip).limit(limit).all()

def get_all_complaints(db: Session, skip: int = 0, limit: int = 100, 
                       plate: str = None, user_email: str = None, status: str = None):
    query = db.query(Complaint)
    if plate:
        query = query.filter(Complaint.plate.contains(plate))
    if status:
        query = query.filter(Complaint.status == status)
    if user_email:
        query = query.join(User).filter(User.email.contains(user_email))
        
    return query.order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_complaint_by_id(db: Session, complaint_id: int):
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()

def update_complaint(db: Session, complaint_id: int, status: str = None, admin_note: str = None):
    db_complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not db_complaint:
        return None

    if status is not None:
        db_complaint.status = status
    if admin_note is not None:
        db_complaint.admin_note = admin_note

    db.commit()
    db.refresh(db_complaint)
    return db_complaint
