from fastapi import APIRouter, Depends

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", status_code=200)
async def health():
    return 1
