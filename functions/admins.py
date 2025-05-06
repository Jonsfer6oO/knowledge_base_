from sqlalchemy import select
from typing import List
from datetime import datetime

from admins import AdminsBase
from configurations import Session
from hash_functions import hashed_password
from .other import convert_dict_in_str
from error_logs import ErrorsBase
from .error_logs import add_errors

def add_admin(obj: AdminsBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - add_admin(obj = {obj})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True

def get_admin(value: int | str, attribute: str = "none") -> AdminsBase | bool:
    """
        Function to get admin objects.

        Parameters:
            -  atribute - may be 'user_id' or 'login';
            -  value - sqarch value.

        Warning:
            If **attribute** == 'none' or other, then search will be **attribute** == 'user_id'.

    """

    with Session() as session:
        try:
            if attribute == "login":
                statement = select(AdminsBase).where(AdminsBase.login==value)
            else:
                statement = select(AdminsBase).where(AdminsBase.id_user==int(value))

            db_object = session.scalars(statement).first()

            _ = db_object.user_admin

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - get_admin(value = {value}, attribute = {attribute})",
                error_date = datetime.now()
            ))

            return False

def get_admin_by_id(id: int) -> AdminsBase | bool:
    with Session() as session:
        try:
            statement = select(AdminsBase).where(AdminsBase.id==int(id))
            db_object = session.scalars(statement).one()

            _ = db_object.user_admin

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - get_admin_by_id(id = {id})",
                error_date = datetime.now()
            ))

            return False

def update_admin(user_id: int, **new_values) -> bool:
    """
        Function for updating admin.

        Parameters:
            -  user_id - admin ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """

    with Session() as session:
        try:
            admin = get_admin(user_id)
            for key, value in new_values.items():
                if hasattr(admin, key):
                    setattr(admin, key, value)

                if new_values.get("password", 0) != 0:
                    salt, hash_pass = hashed_password(new_values["password"])

                    admin.salt = salt
                    admin.password = hash_pass

            session.merge(admin)

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - update_admin(user_id = {user_id}, " +
                        f"**new_values = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

        else:
            session.commit()
            return True

def del_admin(user_id: int):
    with Session() as session:
        try:
            article = get_admin(user_id)
            session.delete(article)
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - del_admin(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True
