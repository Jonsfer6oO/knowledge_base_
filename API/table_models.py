from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


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

    id: int = 0
    login: str
    email: str
    phone: int
    birthday: date
    registration_date: datetime
    rating: float = 0.0

    # article: Optional["ArticlesBase"] = None
    # admin: Optional["AdminsBase"] = None
    # black_list: Optional["BlackListBase"] = None
    # errors: Optional["ErrorsBase"] = None


class User_for_update_api(BaseModel):
    """Model describing the user for update."""

    login: str = "none"
    email: str = "none"
    phone: int | str = "none"
    birthday: date | str = "none"
    registration_date: datetime | str = "none"
    rating: float | str = "none"


class User_for_input_api(BaseModel):
    """Model describing the user for input."""

    login: str
    email: str
    phone: int
    birthday: date
    registration_date: datetime
    rating: float = 0.0

# ---------------------------------------------------- articles --------------------------------------------------