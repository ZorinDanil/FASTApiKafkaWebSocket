from jose import jwt
from passlib.context import CryptContext

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MESSAGE_GET_TOKEN_DATA_403 = 'Could not validate credentials'


class TokenPayload(BaseModel):
    user_id: str


class AuthValidator:
    def __init__(self, secret_key: str, algorithms: list[str]) -> None:
        self._secret_key = secret_key
        self._algorithms = algorithms

    async def validate_token(self, encoded_token: str):
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
            return decoded_token["user_id"]
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")

    async def extract_token_data(
            self,
            token: str
    ) -> TokenPayload:
        try:
            decoded_token = jwt.decode(token, self._secret_key, algorithms=self._algorithms)
            token_data = TokenPayload(**decoded_token)
        except (jwt.JWTError, ValidationError) as error:
            raise HTTPException(status_code=403, detail=str(error))
        return token_data


auth_validator = AuthValidator(settings.SECRET_KEY, [settings.ALGORITHM])
