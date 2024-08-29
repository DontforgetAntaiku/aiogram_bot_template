from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    # lang = Column(String, nullable=False)
    banned = Column(Boolean, default=False)
