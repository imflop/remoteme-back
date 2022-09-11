import dataclasses as dc
import typing as t
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Float,
    Integer,
    String,
    UnicodeText,
    text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from .common import Base, PSQLAEnum
from .users import UserModel


class CurrencyTypeEnum(str, Enum):
    """
    Currencies
    """

    USD = "usd"
    EUR = "eur"
    RUB = "rub"
    GBP = "gbp"
    CNY = "cny"
    UAH = "uah"

    @classmethod
    def get_icon_by_value(cls, val: str) -> str:
        return {"usd": "$", "eur": "€", "gbp": "£", "cny": "¥", "rub": "₽", "uah": "₴"}.get(val) if val else "$"


class TagTypeEnum(str, Enum):
    """
    Tag's types
    """

    STACK = "stack"
    LEVEL = "level"
    SCOPE = "scope"


class TagModel(Base):
    """
    Tags for adverts including technologies (stack), levels, scopes, etc.
    """

    __tablename__ = "jobs_tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    slug_name = Column(String(128))
    code = Column(String(32))
    label = Column(String(32))
    type = Column(PSQLAEnum(TagTypeEnum), nullable=False, server_default=text(f"{TagTypeEnum.SCOPE}"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TagToAdvertModel(Base):
    __tablename__ = "jobs_advert_tags"

    id = Column(Integer, primary_key=True)
    advert_id = Column(Integer, ForeignKey("jobs_advert.id"))
    tag_id = Column(Integer, ForeignKey("jobs_tag.id"))


class AdvertModel(Base):
    """
    Adverts
    """

    __tablename__ = "jobs_advert"

    id: int = Column(Integer, primary_key=True)
    uuid: UUID = Column(UUID(as_uuid=True), default=uuid4)
    short_description: str = Column(String(128), nullable=False)
    slug_short_description: str = Column(String(128), nullable=False)
    long_description = Column(UnicodeText, nullable=False)
    salary_from: int = Column(Integer, server_default=text("0"), nullable=False)
    salary_to: int = Column(Integer, server_default=text("0"), nullable=True)
    currency: str = Column(PSQLAEnum(CurrencyTypeEnum), nullable=False, server_default=text(f"{CurrencyTypeEnum.USD}"))
    company_name: str = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users_user.id"), index=True)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_remote: bool = Column(Boolean, default=False, server_default=text("false"))
    is_moderate: bool = Column(Boolean, default=False, server_default=text("false"))
    city = Column(String(128), nullable=True)
    country = Column(String(128), nullable=True)
    telegram = Column(String(128))
    email = Column(String(254))
    vacancy_source_url = Column(String(200), nullable=True)
    similarity_coefficient = Column(Float, nullable=True)
    similar_adverts = Column(JSONB, nullable=True, server_default=text("'{}'::jsonb"))

    tags = relationship(TagModel, secondary=TagToAdvertModel.__tablename__, backref="adverts")
    user = relationship(UserModel, foreign_keys=[user_id])


@dc.dataclass(frozen=True, repr=False, slots=True)
class Currency:
    code: str
    symbol: str


@dc.dataclass(frozen=True, repr=False, slots=True)
class AdvertSalary:
    from_: int
    to_: int
    currency: Currency


@dc.dataclass(frozen=True, repr=False, slots=True)
class AdvertShort:
    id: int
    uuid: UUID
    company_name: str
    short_description: str
    slug_short_description: str
    tags: t.Sequence[TagModel]
    created_at: datetime
    user: t.Optional[UserModel]
    is_remote: bool
    salary: AdvertSalary

    @classmethod
    def build(cls, advert: AdvertModel) -> t.Any:
        return cls(
            id=advert.id,
            uuid=advert.uuid,
            company_name=advert.company_name,
            short_description=advert.short_description,
            slug_short_description=advert.slug_short_description,
            tags=advert.tags,
            created_at=advert.created_at,
            user=advert.user,
            is_remote=advert.is_remote,
            salary=AdvertSalary(
                from_=advert.salary_from,
                to_=advert.salary_to,
                currency=Currency(code=advert.currency, symbol=CurrencyTypeEnum.get_icon_by_value(advert.currency))
            )
        )
