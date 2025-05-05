from typing import Type, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.future import select

from app.controllers.base import BaseModelController

ModelType = Type[BaseModel]


class ProfileModelController(BaseModelController):

    async def get_by_user_id(
        self, db: AsyncSession, id: Any
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.user_id == id)
        result = await db.execute(query)
        return result.scalars().first()
