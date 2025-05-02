from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from configurations import Base


class AccountsBase(Base):
    """Model describing the user accounts for authentication."""

    __tablename__ = "Accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)