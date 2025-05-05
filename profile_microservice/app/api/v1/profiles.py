from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.profiles import ProfileResponse, ProfileUpdate
from app.api.deps import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers import profile_controller

profile_router = APIRouter()


@profile_router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> ProfileResponse:
    """
    Retrieves a profile by its ID.

    Args:
        user_id (UUID): The ID of the profile to retrieve.

    Returns:
        ProfileResponse: The profile object matching the provided ID.

    Raises:
        HTTPException: If the profile with the given ID is not found in
        the database.
    """
    profile = await profile_controller.get_by_user_id(session, id=user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse.from_orm(profile)


@profile_router.get("/", response_model=List[ProfileResponse])
async def get_profiles(
    session: AsyncSession = Depends(get_session)
) -> List[ProfileResponse]:
    """
    Retrieves all profiles.

    Returns:
        List[ProfileResponse]: The list of all profiles.

    Raises:
        HTTPException: If no profiles are found in the database.
    """
    profiles = await profile_controller.get_multi(session)
    if not profiles:
        raise HTTPException(status_code=404, detail="Profiles not found")
    return profiles


@profile_router.put("/{user_id}", response_model=ProfileResponse)
async def update_profile(
    user_id: UUID,
    profile_update: ProfileUpdate,
    session: AsyncSession = Depends(get_session)
) -> ProfileResponse:
    """
    Updates a profile by user ID.

    Args:
        user_id (UUID): The ID of the profile to update.

    Returns:
        ProfileResponse: The updated profile object.

    Raises:
        HTTPException: If the profile with the given ID is
            not found in the database.
    """
    profile = await profile_controller.get_by_user_id(session, user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    updated_profile = await profile_controller.update(
        session, db_obj=profile, obj_in=profile_update
    )

    return ProfileResponse.from_orm(updated_profile)


@profile_router.patch("/{user_id}", response_model=ProfileResponse)
async def patch_profile(
    user_id: UUID,
    profile_update: ProfileUpdate,
    session: AsyncSession = Depends(get_session)
) -> ProfileResponse:
    """
    Patch a profile by user ID.

    Args:
        user_id (UUID): The ID of the profile to update.

    Returns:
        ProfileResponse: The updated profile object.

    Raises:
        HTTPException: If the profile with the given ID is
            not found in the database.
    """
    profile = await profile_controller.get_by_user_id(session, user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    print(profile_update)
    updated_profile = await profile_controller.patch(
        session, db_obj=profile, obj_in=profile_update
    )
    return ProfileResponse.from_orm(updated_profile)
