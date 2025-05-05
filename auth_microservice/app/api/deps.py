from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.users import User

from app.core.security import auth_validator

extract_token_data = auth_validator.extract_token_data


async def get_session() -> SessionLocal:
    async with SessionLocal() as session:
        yield session


async def get_current_user(
        token: str = Depends(extract_token_data),
        session: AsyncSession = Depends(get_session),
) -> User:
    user = await session.get(User, token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=settings.GET_CURRENT_USER_404)
    return user
