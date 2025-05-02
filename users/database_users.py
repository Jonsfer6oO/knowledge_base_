from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, DateTime, Float, BLOB
from sqlalchemy import ForeignKey

from typing import List, Optional
from datetime import date, datetime

from configurations import Base


class UsersBase(Base):
    """Model describing the user."""

    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)  # Mapped - транслирует тип данных python в SQL
    login: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(Integer(), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column(Date(), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)

    # Устанавливает связь с атрибутами указанной таблицы на уровне python
    # back_populates - помогает при обновлении данных в одной из таблиц
    article: Mapped[List["Child"]] = relationship("Articles", back_populates="user")
    admin: Mapped[List["Child"]] = relationship("Admins", back_populates="user_admin", uselist=False)
    black_list: Mapped[List["Child"]] = relationship("BlackList", back_populates="user_black", uselist=False)


class ArticlesBase(Base):
    """Model describing the user articles."""

    __tablename__ = "Articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("Users.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(BLOB(20000), nullable=False)
    co_author_login: Mapped[Optional[str]] = mapped_column(String(30))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer())
    creation_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)

    user: Mapped[List["Child"]] = relationship("Users", back_populates="article")
