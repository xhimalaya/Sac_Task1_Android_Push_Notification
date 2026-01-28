from pydantic import BaseModel
from typing import Optional, Dict


class NotifyAllRequest(BaseModel):
    title: str
    message: str
    data: Optional[Dict] = None
