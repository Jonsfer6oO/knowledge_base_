from sqlalchemy import select
from typing import List
from datetime import datetime

from accounts import AccountsBase
from configurations import Session
from crypto import hashed_password
from .other import convert_dict_in_str
from error_logs import ErrorsBase
from .error_logs import add_errors

def add_account(obj: AccountsBase):
    with Session() as session:
        try:
            session.add(obj)
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - add_account(obj = {obj})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True

def get_account(value: int | str, attribute: str = "none") -> AccountsBase | None | bool:
    """
        Function to get account objects.

        Parameters:
            -  atribute - may be 'id' or 'login';
            -  value - sqarch value.

        Warning:
            If **attribute** == 'none' or other, then search will be **attribute** == 'id'.

    """

    with Session() as session:
        try:
            if attribute == "login":
                statement = select(AccountsBase).where(AccountsBase.login==value)
            else:
                statement = select(AccountsBase).where(AccountsBase.id==int(value))

            db_object = session.scalars(statement).one_or_none()

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - get_account(value = {value}, attribute = {attribute})",
                error_date = datetime.now()
            ))

            return False

def update_account(id: int, **new_values) -> bool | None:
    """
        Function for updating admin.

        Parameters:
            -  id - account ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """

    with Session() as session:
        try:
            account = get_account(id)
            if account != None:
                for key, value in new_values.items():
                    if hasattr(account, key):
                        setattr(account, key, value)

                    if new_values.get("password", 0) != 0:
                        salt, hash_pass = hashed_password(new_values["password"])

                        account.salt = salt
                        account.password = hash_pass
            else:
                return None

            session.merge(account)

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - update_account(id = {id}, " +
                        f"**new_value = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

        else:
            session.commit()
            return True

def del_account(id: int) -> bool | None:
    with Session() as session:
        try:
            account = get_account(id)
            if account != None:
                session.delete(account)
            else:
                return None

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - del_account(id = {id})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True