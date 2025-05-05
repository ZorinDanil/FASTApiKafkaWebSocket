import datetime
from typing import Type, Any, List, Union, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select

ModelType = Type[BaseModel]
CreateSchemaType = Type[BaseModel]
UpdateSchemaType = Type[BaseModel]


class BaseModelController():
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, db: AsyncSession, id: Any
    ) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_user_id(
        self, db: AsyncSession, id: Any
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.user_id == id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj: ModelType = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Convert all datetime objects to UTC
        for key, value in update_data.items():
            if isinstance(value, datetime.datetime):
                if value.tzinfo is None:
                    update_data[key] = value.replace(
                        tzinfo=datetime.timezone.utc
                        )
                else:
                    update_data[key] = value.astimezone(datetime.timezone.utc)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def patch(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        data_dict = obj_in.dict(exclude_unset=True)

        # Convert all datetime objects to UTC
        for key, value in data_dict.items():
            if isinstance(value, datetime.datetime):
                data_dict[key] = value.replace(tzinfo=None)

        for key, value in data_dict.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def remove(
        self,
        db: AsyncSession,
        *,
        id: Any,
    ) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(
            self.model.id == id))
        db_obj = result.scalars().first()
        if db_obj is not None:
            await db.delete(db_obj)
            await db.commit()
        return db_obj
