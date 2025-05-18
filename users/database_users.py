from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, DateTime, Float, BLOB
from sqlalchemy import ForeignKey

from typing import List, Optional
from datetime import date, datetime

from configurations import Base


class UsersBase(Base):
    """Model describing the user."""

    __tablename__ = "Users"

    def __init__(self, **kw):
        """
            Creating a user object.

            Parameters:
                login (str): Unique username (3-30 characters).
                email (str): Unique email address (max 50 characters).
                phone (str): Unique phone number (integer value stored as string).
                birthday (date): User's date of birth.
                registration_date (datetime): Date and time of registration.
                rating (float): User rating score.
                id (Optional[int]): Auto-generated primary key if None. Defaults to None.
        """

        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

    id: Mapped[int] = mapped_column(primary_key=True)  # Mapped - транслирует тип данных python в SQL
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(Integer(), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column(Date(), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)


    # Устанавливает связь с атрибутами указанной таблицы на уровне python
    # back_populates - помогает при обновлении данных в одной из таблиц
    article: Mapped[List["Child"]] = relationship("ArticlesBase",  # type: ignore
                                                  back_populates="user")
    admin: Mapped["Child"] = relationship("AdminsBase",  # type: ignore
                                          back_populates="user_admin",
                                          uselist=False)
    black_list: Mapped["Child"] = relationship("BlackListBase",  # type: ignore
                                               back_populates="user_black",
                                               uselist=False)
    errors: Mapped[List["Child"]] = relationship("ErrorsBase", # type: ignore
                                                 back_populates="user_errors")

    def __str__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"


class ArticlesBase(Base):
    """Model describing the user articles."""

    __tablename__ = "Articles"

    def __init__(self, **kw):
        """
            Creating a user articles.

            Parameters:
                user_id (int): ID of the author (foreign key to Users table)
                title (str): Article title (max 100 characters)
                text (str): Article content (max 20,000 bytes as BLOB)
                creation_date (datetime): Date and time when article was created
                rating (float): Article rating score
                co_author_login (Optional[str]): Login of co-author (max 30 chars). Defaults to None.
                parent_id (Optional[int]): ID of parent article for replies/versions. Defaults to None.
                id (Optional[int]): Auto-generated primary key if None. Defaults to None.
        """

        for key, value in kw.items():
            if key == "text":
                value = bytes(value, "utf-8")
            if hasattr(self, key):
                setattr(self, key, value)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(BLOB(20000), nullable=False)
    co_author_login: Mapped[Optional[str]] = mapped_column(String(30))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer())
    creation_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)

    user: Mapped["Parent"] = relationship("UsersBase", back_populates="article") # type: ignore

    def __str__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"
