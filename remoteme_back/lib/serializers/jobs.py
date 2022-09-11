import typing as t
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .users import User


class Tag(BaseModel):
    id: int
    name: str
    slug_name: str
    code: t.Optional[str]
    label: t.Optional[str]
    type: str

    class Config:
        orm_mode = True


class Currency(BaseModel):
    code: str
    symbol: str

    class Config:
        orm_mode = True


class AdvertBase(BaseModel):
    id: int
    uuid: UUID
    company_name: str
    short_description: str
    slug_short_description: str
    created_at: datetime
    user: t.Optional[User]
    is_remote: bool


class Salary(BaseModel):
    from_: int
    to_: t.Optional[int]
    currency: Currency

    class Config:
        orm_mode = True


class Advert(AdvertBase):
    tags: t.Sequence[Tag]
    salary: Salary

    class Config:
        orm_mode = True


class DetailedAdvert(AdvertBase):
    tags: t.Sequence[Tag]
    salary_from: int
    salary_to: int | None
    city: str | None

    class Config:
        orm_mode = True


class PaginatedAdvert(BaseModel):
    limit: int
    offset: int
    count: int
    result: t.Sequence[Advert]
