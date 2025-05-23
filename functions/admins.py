from sqlalchemy import select
from typing import List
from datetime import datetime

from admins import AdminsBase
from configurations import Session
from crypto import hashed_password
from .other import convert_dict_in_str
from error_logs import ErrorsBase
from .error_logs import add_errors

def add_admin(obj: AdminsBase) -> AdminsBase | bool:
    with Session() as session:
        try:
            session.add(obj)

            session.commit()
            session.refresh(obj)

            return obj

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - add_admin(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_admin(value: int | str, attribute: str = "none") -> AdminsBase | None | bool:
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

            db_object = session.scalars(statement).one_or_none()

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

def get_admin_by_id(id: int) -> AdminsBase | None | bool:
    with Session() as session:
        try:
            statement = select(AdminsBase).where(AdminsBase.id==int(id))
            db_object = session.scalars(statement).one_or_none()

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

def update_admin(user_id: int, **new_values) -> bool | None:
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
            if admin != None:
                for key, value in new_values.items():
                    if hasattr(admin, key) and value != None:
                        setattr(admin, key, value)

                    if new_values.get("password") != None:
                        salt, hash_pass = hashed_password(new_values["password"])

                        admin.salt = salt
                        admin.password = hash_pass
            else:
                return None

            session.merge(admin)

            session.commit()
            return True

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

def del_admin(user_id: int) -> bool | None:
    with Session() as session:
        try:
            admin = get_admin(user_id)
            if admin != None:
                session.delete(admin)
            else:
                return None

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
