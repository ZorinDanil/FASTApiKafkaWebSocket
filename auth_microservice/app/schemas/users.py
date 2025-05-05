from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str | None
    email: str | None
    is_active: bool | None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
