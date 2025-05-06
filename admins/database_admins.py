from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from typing import List

from configurations import Base
from hash_functions import hashed_password


class AdminsBase(Base):
    """Model describing the admins."""

    __tablename__ = "Admins"

    def __init__(self, **kw):
        """Initialize a new admin instance.

        Parameters:
            id_user (int): Reference to parent user if applicable.
            login (str): Unique username (3-30 characters)
            password (str): User password (will be hashed before storage)
            id (Optional[int]): Auto-incremented primary key. Defaults to None.
        """

        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

            salt, hash_pass = hashed_password(kw["password"])
            setattr(self, "salt", salt)
            setattr(self, "password", hash_pass)


    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    salt: Mapped[bytes] = mapped_column(LargeBinary(16), nullable=False)

    user_admin: Mapped["Parent"] = relationship("UsersBase", back_populates="admin", uselist=False) # type: ignore

    def __str__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"