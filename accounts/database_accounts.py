from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from configurations import Base


class AccountsBase(Base):
    """Model describing the user accounts for authentication."""

    __tablename__ = "Accounts"

    def __init__(self, **kw):
        """Initialize a new User instance with secure password storage.

        Parameters:
            login (str): Unique username (3-30 characters, case-sensitive)
            password (str): Plain-text password (will be hashed before storage)
            id (Optional[int]): Auto-incremented primary key. Defaults to None.
        """

        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)