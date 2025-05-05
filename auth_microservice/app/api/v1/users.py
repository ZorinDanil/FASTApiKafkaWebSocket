import uuid
from app.api.deps import get_session
from app.core.security import auth_validator
from app.kafka_config.kafka_producer import kafka_producer
from app.models.users import User as UserModel
from app.schemas.users import User as UserSchema
from app.schemas.users import UserCreate as UserCreateSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from sqlalchemy import exc

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema],
            dependencies=[Depends(auth_validator.extract_token_data)])
async def get_all_users(session: AsyncSession = Depends(get_session)
                        ) -> List[UserSchema]:
    """
    Retrieve all users
    """
    users = await session.execute(select(UserModel))
    return users.scalars().all()


@router.get("/{user_id}", response_model=UserSchema,
            dependencies=[Depends(auth_validator.extract_token_data)])
async def get_user_by_id(user_id: str,
                         session: AsyncSession = Depends(get_session)):
    """
    Get user by ID
    """
    user = await session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserSchema)
async def create_user(
        user_data: UserCreateSchema,
        session: AsyncSession = Depends(get_session),
):
    """
    Create a new user
    """
    user = UserModel(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        hashed_password=await auth_validator.hash_password(user_data.password)
    )
    try:
        session.add(user)
        await session.commit()
        kafka_data = {"type": "user_created", "user": user.dict()}
        await kafka_producer.send('user_events', kafka_data)
    except exc.IntegrityError:
        raise HTTPException(status_code=400,
                            detail="User with this username already exists")
    return UserSchema.from_orm(user)
