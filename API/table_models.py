from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Union


from users import UsersBase, ArticlesBase
from admins import AdminsBase
from black_list import BlackListBase
from error_logs import ErrorsBase


class Response_model(BaseModel):
    type: str
    data: dict

# ---------------------------------------------------- users --------------------------------------------------

class User_api(BaseModel):
    """Model describing the user."""

    id: int
    login: str
    email: str
    phone: int
    birthday: date
    registration_date: datetime
    rating: float

    # article: Optional["ArticlesBase"] = None
    # admin: Optional["AdminsBase"] = None
    # black_list: Optional["BlackListBase"] = None
    # errors: Optional["ErrorsBase"] = None


class User_for_update_api(BaseModel):
    """Model describing the user for update."""

    login: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    birthday: Optional[date] = None
    registration_date: Optional[datetime] = None
    rating: Optional[float] = None


class User_for_input_api(BaseModel):
    """Model describing the user for input."""

    login: str
    email: str
    phone: int
    birthday: date
    registration_date: datetime
    rating: float = 0.0

# ---------------------------------------------------- articles --------------------------------------------------

class Article_api(BaseModel):
    """Model describing the user article."""

    id: int
    user_id: int
    title: str
    text: str
    creation_date: datetime
    rating: float
    co_author_login: Optional[str] = None
    parent_id: Optional[int] = None

    #user: Optional["UsersBase"] = None


class Article_for_update_api(BaseModel):
    """Model describing the user article for update."""

    user_id: Optional[int] = None
    title: Optional[str] = None
    text: Optional[str] = None
    creation_date: Optional[datetime] = None
    rating: Optional[float] = None
    co_author_login: Optional[str] = None
    parent_id: Optional[int] = None


class Article_for_input_api(BaseModel):
    """Model describing the user for input."""

    user_id: int
    title: str
    text: str
    creation_date: datetime
    rating: float
    co_author_login: Optional[str] = None
    parent_id: Optional[int] = None

# ---------------------------------------------------- error logs --------------------------------------------------

class Error_api(BaseModel):
    """Model describing the error logs."""

    id: int
    id_user: int
    message: str
    event: str
    error_date: datetime


class Error_for_input_api(BaseModel):
    """Model describing the error logs for update."""

    id_user: int
    message: str
    event: str
    error_date: datetime

# ---------------------------------------------------- admins --------------------------------------------------

class Admin_api(BaseModel):
    """Model describing the admins."""

    id: int
    id_user: int
    login: str
    password: str
    salt: str


class Admin_for_input_api(BaseModel):
    """Model describing the admins for input."""

    id_user: int
    login: str
    password: str


class Admin_for_update_api(BaseModel):
    """Model describing the admins for update."""

    id_user: Optional[int] = None
    login: Optional[str] = None
    password: Optional[str] = None

# ---------------------------------------------------- accounts --------------------------------------------------

class Account_api(BaseModel):
    """Model describing the account."""

    id: int
    login: str
    password: str
    salt: str


class Account_for_input_api(BaseModel):
    """Model describing the account for input."""

    login: str
    password: str


class Account_for_update_api(BaseModel):
    """Model describing the account for update."""

    login: Optional[str] = None
    password: Optional[str] = None

# ---------------------------------------------------- black_list --------------------------------------------------

class Black_list_api(BaseModel):
    """Model describing user in black list."""

    id: int
    id_user: int
    cause: str
    date_add: datetime


class Black_list_for_input_api(BaseModel):
    """Model describing user in black list for input."""

    id_user: int
    cause: str
    date_add: datetime


class Black_list_for_update_api(BaseModel):
    """Model describing user in black list for update."""

    id_user: Optional[int] = None
    cause: Optional[str] = None
    date_add: Optional[datetime] = None
