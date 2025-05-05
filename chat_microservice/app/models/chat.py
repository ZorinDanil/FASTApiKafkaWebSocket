# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId


class Chat(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    participants: List[str]
    messages: List[str] = []
