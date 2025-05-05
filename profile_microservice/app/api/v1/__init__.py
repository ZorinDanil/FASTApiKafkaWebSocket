from fastapi import APIRouter

from app.api.v1.profiles import profile_router

router = APIRouter(prefix="/v1")

router.include_router(profile_router)
