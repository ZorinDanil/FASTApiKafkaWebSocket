from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Message(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()))
    chat_id: str
    sender_id: str
    content: str
