from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)  # Changed from full_name to name
    is_active = Column(Boolean, default=True)
    role = Column(String, default="officer")  # Changed from is_admin to role: "admin" or "officer"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    complaints = relationship("Complaint", back_populates="owner")

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    plate = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(String, nullable=False)  # Date as string in DD.MM.YYYY format
    location = Column(String, nullable=False)  # Full combined address string
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)
    address_detail = Column(String, nullable=True)
    status = Column(String, default="İnceleniyor")  # Turkish status: İnceleniyor, Onaylandı, Reddedildi
    admin_note = Column(Text, nullable=True)  # Admin decision note
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="complaints")
