from pydantic import BaseModel

from src.models.emums import RoleEnum


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.user


class Token(BaseModel):
    access_token: str
    token_type: str
