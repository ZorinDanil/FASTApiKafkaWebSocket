import datetime
import uuid

from sqlalchemy import UUID, Column, String, DateTime, Text
from app.models.base import Base


class Profile(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(Text, nullable=True)
    lastname = Column(Text, nullable=True)
    birthday = Column(DateTime, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
