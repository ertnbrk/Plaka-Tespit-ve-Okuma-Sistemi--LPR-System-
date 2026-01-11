from pydantic import BaseModel
from typing import Optional, Dict

class Token(BaseModel):
    token: str  # Changed from access_token to token
    user: Dict  # User object with id, name, email, role

class TokenData(BaseModel):
    email: Optional[str] = None
