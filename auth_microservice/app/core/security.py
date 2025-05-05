from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.users import User
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MESSAGE_GET_TOKEN_DATA_403 = 'Could not validate credentials'


class AuthValidator:
    def __init__(self, secret_key: str, algorithms: list[str]) -> None:
        self._secret_key = secret_key
        self._algorithms = algorithms

    async def validate_token(self, encoded_token: str) -> TokenPayload:
        """
        Validates the provided JWT token.

        Args:
            encoded_token (str): The encoded JWT token.

        Raises:
            HTTPException: If the token is invalid or expired.

        Returns:
            TokenPayload: The decoded payload of the token.
        """
        try:
            decoded_token = jwt.decode(
                encoded_token, self._secret_key, algorithms=self._algorithms
            )
            return TokenPayload(user_id=decoded_token["user_id"])
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")

    @staticmethod
    async def create_access_token(user: User) -> str:
        """
        Create an access token for a user.

        Args:
            user (User): The user for whom the token is being created.

        Returns:
            str: The generated access token.
        """
        expiration_time = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_payload = {"exp": expiration_time, "user_id": str(user.id)}
        secret_key = settings.SECRET_KEY.get_secret_value()
        algorithm = settings.ALGORITHM
        token = jwt.encode(token_payload, secret_key, algorithm=algorithm)
        print(token)
        return token
    
    @staticmethod
    async def check_password(plain_password: str, hashed_password: str) -> bool:
        """
        Check if a plain password matches a hashed password.

        Args:
            plain_password (str): The plain password to check.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def hash_password(plain_password: str) -> str:
        """
        Hash a plain password.

        Args:
            plain_password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(plain_password)
    
    async def extract_token_data(
            self,
            token: str = Depends(
                OAuth2PasswordBearer()
            )
    ) -> TokenPayload:
        try:
            decoded_token = jwt.decode(token, self._secret_key, algorithms=self._algorithms)
            token_data = TokenPayload(**decoded_token)
        except (jwt.JWTError, ValidationError) as error:
            raise HTTPException(status_code=403, detail=str(error))
        return token_data

    async def authenticate(
            self, session: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        result = await session.execute(select(User).filter_by(username=username))
        user = result.scalars().first()
        if user and await self.check_password(password, user.hashed_password):
            return user
        return None


auth_validator = AuthValidator(settings.SECRET_KEY.get_secret_value(), [settings.ALGORITHM])
