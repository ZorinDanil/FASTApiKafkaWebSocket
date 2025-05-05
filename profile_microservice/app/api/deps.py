from app.core.database import SessionLocal


async def get_session() -> SessionLocal:  # type: ignore
    async with SessionLocal() as session:
        yield session
