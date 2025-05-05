from typing import List
from pydantic import BaseModel


class ChatCreate(BaseModel):
    participants: List[str]
