from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db.models.base import Base
from src.models.emums import RoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(64), unique=True)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(10), nullable=False, default=RoleEnum.user)
