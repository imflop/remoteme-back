from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    Integer,
    String,
    UnicodeText,
    text
)

from .common import Base


class UserModel(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    date_joined = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    username = Column(String(150))
    email = Column(String(254))
