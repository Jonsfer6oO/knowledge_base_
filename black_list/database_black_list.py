from sqlalchemy import String, Integer, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from datetime import datetime
from typing import List

from configurations import Base


class BlackListBase(Base):
    """Model describing black list."""

    __tablename__ = "BlackList"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    cause: Mapped[str] = mapped_column(String(200), nullable=False)
    date_add: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    user_black: Mapped[List["Child"]] = relationship("Users", back_populates="black_list",  uselist=False)