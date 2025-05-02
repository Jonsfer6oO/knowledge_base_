from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from datetime import datetime
from typing import List

from configurations import Base


class ErrorsBase(Base):
    """Model describing the errors."""

    __tablename__ = "Errors"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    message: Mapped[str] = mapped_column(Text(1000), nullable=False)
    event: Mapped[str] = mapped_column(String(100), nullable=False)
    error_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    user: Mapped[List["Child"]] = relationship("Users")
