from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union

class CookieCreate(BaseModel):
    domain: str
    username: str
    cookie_data: Dict[str, Any] | List[Dict[str, Any]]

class CookieResponse(BaseModel):
    success: bool
    message: str
    data: Optional[List[Dict[str, Any]]] = None 

class StorageCreate(BaseModel):
    domain: str
    username: str
    storage_data: dict

class StorageResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None 