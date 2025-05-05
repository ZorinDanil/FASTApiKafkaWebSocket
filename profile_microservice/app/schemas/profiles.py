from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ProfileBase(BaseModel):
    name: str | None = None
    lastname: str | None = None
    birthday: datetime | None = None
    profile_picture_url: str | None = None

    class Config:
        from_attributes = True


class ProfileResponse(ProfileBase):
    id: UUID | None
    user_id: UUID | None
    created_at: datetime | None
    updated_at: datetime | None


class ProfileUpdate(ProfileBase):
    ...
