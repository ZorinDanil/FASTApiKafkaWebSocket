import uuid
from sqlalchemy import UUID, Boolean, Column, String

from app.models.base import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False)
    email = Column(String, index=True, unique=True)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
