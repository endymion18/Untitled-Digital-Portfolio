from typing import List

from src.database import Base
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(length=500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
