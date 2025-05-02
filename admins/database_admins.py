from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from typing import List

from configurations import Base


class AdminsBase(Base):
    """Model describing the admins."""

    __tablename__ = "Admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    user_admin: Mapped[List["Child"]] = relationship("Users", back_populates="admin", uselist=False)