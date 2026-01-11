from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComplaintBase(BaseModel):
    plate: str
    description: str
    date: str  # Date as string in DD.MM.YYYY format
    location: str  # Full combined address
    city: Optional[str] = None
    district: Optional[str] = None
    neighborhood: Optional[str] = None
    address_detail: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None  # İnceleniyor, Onaylandı, Reddedildi
    admin_note: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: int
    user_id: int
    status: str
    admin_note: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
