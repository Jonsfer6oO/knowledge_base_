from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from datetime import datetime

from configurations import Base


class ErrorsBase(Base):
    """Model describing the errors."""

    __tablename__ = "Errors"

    def __init__(self, **kw):
        """Initialize a new ErrorLog entry.

        Parameters:
            id_user (int): ID of the user associated with the error (foreign key to Users table)
            message (str): Detailed error message (max 1000 characters)
            event (str): Name or type of the event that caused the error (max 100 characters)
            error_date (datetime): Date and time when the error occurred
            id (Optional[int]): Auto-generated primary key if None. Defaults to None.
        """
        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    message: Mapped[str] = mapped_column(Text(1000), nullable=False)
    event: Mapped[str] = mapped_column(String(500), nullable=False)
    error_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    user_errors: Mapped["Parent"] = relationship("UsersBase", back_populates="errors")  # type: ignore
