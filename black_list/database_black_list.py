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

    def __init__(self, **kw):
        """Initialize a new user in black list.

        Parameters:
            id_user (int): ID of the user who performed the action (references Users.id)
            cause (str): Description of the action/event (max 200 characters)
            date_add (datetime): Timestamp when the action was logged
            id (Optional[int]): Auto-incremented primary key. Defaults to None.
        """
        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    cause: Mapped[str] = mapped_column(String(200), nullable=False)
    date_add: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    user_black: Mapped["Parent"] = relationship("UsersBase", back_populates="black_list",  uselist=False) # type: ignore