from fastapi import Form

from .errors import unauthed_exc
from crypto import validate_password
from functions import get_account, get_user
from users import UsersBase

def valid_auth_user(login: str = Form(),
                    password: str = Form()) -> UsersBase | bool:
    account = get_account(login, "login")

    if account == None:
        raise unauthed_exc
    if validate_password(secret=account.password,
                         salt=account.salt,
                         password=password):

        return get_user(login, "login")
