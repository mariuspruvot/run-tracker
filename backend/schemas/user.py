from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import uuid


class Birthdate(BaseModel):
    year: Annotated[int, Field(..., ge=1900, le=datetime.now().year)] | None = None
    month: Annotated[int, Field(..., ge=1, le=12)] | None = None
    day: Annotated[int, Field(..., ge=1, le=31)] | None = None


class UserInformation(BaseModel):
    birthdate: Optional[Birthdate] = Field(default_factory=Birthdate)
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    password: str
    additional_information: Optional[UserInformation] = Field(
        default_factory=UserInformation
    )

    class Config:
        extra_fields = "forbid"


class UpdateUserInDB(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    additional_information: Optional[UserInformation] = Field(
        default_factory=UserInformation
    )

    class Config:
        extra_fields = "forbid"


class UserOutDB(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    birthdate: str | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_code: str | None = None

    class Config:
        from_attributes = True
