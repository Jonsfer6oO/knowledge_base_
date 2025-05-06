from sqlalchemy import select
from datetime import datetime

from black_list import BlackListBase
from configurations import Session
from .error_logs import add_errors
from error_logs import ErrorsBase
from .other import convert_dict_in_str

def add_black_list(obj: BlackListBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - add_black_list(obj = {obj})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True

def get_user_black_list_id(id: int) -> BlackListBase | bool:
    with Session() as session:
        try:
            statement = select(BlackListBase).where(BlackListBase.id==int(id))
            db_object = session.scalars(statement).first()

            _ = db_object.user_black

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - get_user_black_list_id(id = {id})",
                error_date = datetime.now()
            ))

            return False

def get_user_black_list_user_id(user_id: int) -> BlackListBase | bool:
    with Session() as session:
        try:
            statement = select(BlackListBase).where(BlackListBase.id_user==int(user_id))
            db_object = session.scalars(statement).first()

            _ = db_object.user_black

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - get_user_black_list_user_id(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False

def update_user_black_list(user_id: int, **new_values) -> bool:
    """
        Function for updating user in black list.

        Parameters:
            -  id - user ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """
    with Session() as session:
        try:
            user_black_list = get_user_black_list_user_id(user_id)
            for key, value in new_values.items():
                if hasattr(user_black_list, key):
                    setattr(user_black_list, key, value)

            session.merge(user_black_list)

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - update_user_black_list(user_id = {user_id}, " +
                        f"**new_values = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

        else:
            session.commit()
            return True

def del_user_black_list(user_id: int) -> bool:
    with Session() as session:
        try:
            user_black_list = get_user_black_list_user_id(user_id)
            session.delete(user_black_list)
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - del_user_black_list(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False
        else:
            session.commit()
            return True