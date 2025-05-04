from sqlalchemy import select

from black_list import BlackListBase
from configurations import Session

def add_black_list(obj: BlackListBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)
        except:
            session.rollback()
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

        except:
            return False

def get_user_black_list_user_id(user_id: int) -> BlackListBase | bool:
    with Session() as session:
        try:
            statement = select(BlackListBase).where(BlackListBase.id_user==int(user_id))
            db_object = session.scalars(statement).first()

            _ = db_object.user_black

            return db_object

        except:
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

        except:
            session.rollback()
            return False

        else:
            session.commit()
            return True

def del_user_black_list(user_id: int) -> bool:
    with Session() as session:
        try:
            user_black_list = get_user_black_list_user_id(user_id)
            session.delete(user_black_list)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True