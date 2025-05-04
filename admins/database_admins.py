from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from typing import List

from configurations import Base


class AdminsBase(Base):
    """Model describing the admins."""

    __tablename__ = "Admins"

    def __init__(self, **kw):
        """Initialize a new admin instance.

        Parameters:
            login (str): Unique username (3-30 characters)
            password (str): User password (will be hashed before storage)
            id_user (Optional[int]): Reference to parent user if applicable. Defaults to None.
            id (Optional[int]): Auto-incremented primary key. Defaults to None.
        """

        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)


    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    user_admin: Mapped["Parent"] = relationship("Users", back_populates="admin", uselist=False) # type: ignore