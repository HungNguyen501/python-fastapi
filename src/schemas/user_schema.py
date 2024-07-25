from uuid import UUID
from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str | None = None


class UserCreate(UserUpdate):
    name: str


class UserInDB(UserCreate):
    uuid: UUID

class UserChangeGeneralResonpse(BaseModel):
    message: str
