from typing import Literal

from pydantic import BaseModel


class AuthenticationSuccessResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    id: str
    username: str


class TokenPayload(BaseModel):
    user_id: str
