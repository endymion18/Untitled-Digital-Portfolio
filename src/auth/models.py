from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

from typing import List


class UserInfo(Base):
    __tablename__ = "user_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    is_designer: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    city: Mapped[str] = mapped_column(String(length=150), nullable=True)
    description: Mapped[str] = mapped_column(String(length=350), nullable=True)
    # favourite: Mapped[List[int]] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship(back_populates="user_info")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class Avatar(Base):
    __tablename__ = "avatar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String(length=500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="avatar")


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user_info: Mapped["UserInfo"] = relationship(back_populates="user")
    avatar: Mapped["Avatar"] = relationship(back_populates="user")
