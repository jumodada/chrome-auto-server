from pydantic import BaseModel
from typing import Optional, Dict, Any

class CookieCreate(BaseModel):
    domain: str
    username: str
    cookie_data: Dict[str, Any]

class CookieResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None 