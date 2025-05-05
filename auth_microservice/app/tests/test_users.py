import pytest

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from tests.factories import UserFactory
from app.core.config import settings


@pytest.mark.asyncio
async def test_list_users(
    client: AsyncSession,
    session: AsyncConnection,
    user_token_headers: dict[str, str],
) -> None:
    """Test that users can be listed."""
    user_1 = UserFactory(username="charly", hashed_password="124567")
    user_2 = UserFactory(username="jazz", hashed_password="124567")
    session.add_all([user_1, user_2])
    await session.commit()

    response = await client.get("/api/v1/users/", headers=user_token_headers)
    users = response.json()

    assert response.status_code == 200
    assert len(users) == 3

    for user in users:
        assert "password_hashed" not in user
        assert "username" in user
        assert "id" in user


@pytest.mark.asyncio
async def test_list_users_without_authorization(client: AsyncSession, session: AsyncConnection):
    users = [UserFactory(username="charly", hashed_password="124567"), 
             UserFactory(username="jazz", hashed_password="124567")]
    session.add_all(users)
    await session.commit()

    response = await client.get("/api/v1/users/")
    data = response.json()

    assert response.status_code == 401
    assert len(data) == 1
    assert data["detail"] == settings.OAUTH2_NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_users_forbidden(client: AsyncSession, session: AsyncConnection):
    user_1 = UserFactory(username="charly", hashed_password="124567")
    user_2 = UserFactory(username="jazz", hashed_password="124567")
    session.add_all([user_1, user_2])
    await session.commit()

    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": "Bearer InvalidToken"}
    )

    data = response.json()

    assert response.status_code == 403
    assert len(data) == 1
    assert data["detail"] == settings.GET_TOKEN_DATA_403


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncSession, session: AsyncConnection, headers: dict[str, str]):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()
    response = await client.get(f"/api/v1/users/{user.id}", headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == user.username
    assert data["id"] == user.id


@pytest.mark.asyncio
async def test_get_user_by_id_unauthorized(client: AsyncSession, session: AsyncConnection, headers: dict[str, str]):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()

    response = await client.get(f"/api/v1/users/{user.id}", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == settings.OAUTH2_NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_user_by_id_no_authorization(client: AsyncSession, session: AsyncConnection):
    user = UserFactory(username="charly", hashed_password="124567")
    session.add(user)
    await session.commit()

    response = await client.get(f"/api/v1/users/{user.id}")
    data = response.json()

    assert response.status_code == 401
    assert data["detail"] == settings.OAUTH2_NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client: AsyncSession, session: AsyncConnection, user_token_headers: dict[str, str]):
    response = await client.get("/api/v1/users/2", headers=user_token_headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user(client: AsyncSession, session: AsyncConnection):
    user_data = {
        "username": 'charlyfunk',
        "password": 'charlyfunk',
    }
    response = await client.post(f"/api/v1/users/", json=user_data)
    assert response.status_code == 201
