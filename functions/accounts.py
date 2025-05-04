from sqlalchemy import select
from typing import List

from accounts import AccountsBase
from configurations import Session
from hash_functions import hashed_password

def add_account(obj: AccountsBase):
    with Session() as session:
        try:
            session.add(obj)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True

def get_account(value: int | str, attribute: str = "none") -> AccountsBase | bool:
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

            db_object = session.scalars(statement).first()

            return db_object

        except:
            return False


def update_account(id: int, **new_values) -> bool:
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
            admin = get_account(id)
            for key, value in new_values.items():
                if hasattr(admin, key):
                    setattr(admin, key, value)

                if new_values.get("password", 0) != 0:
                    salt, hash_pass = hashed_password(new_values["password"])

                    admin.salt = salt
                    admin.password = hash_pass

            session.merge(admin)

        except:
            session.rollback()
            return False

        else:
            session.commit()
            return True

def del_account(id: int):
    with Session() as session:
        try:
            account = get_account(id)
            session.delete(account)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True