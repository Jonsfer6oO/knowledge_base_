from sqlalchemy import select
from typing import List

from admins import AdminsBase
from configurations import Session

def add_admin(obj: AdminsBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)
        except:
            session.rollback()
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

        except:
            return False

def get_admin_by_id(int: id) -> AdminsBase | bool:
    with Session() as session:
        try:
            statement = select(AdminsBase).where(AdminsBase.id==int(id))
            db_object = session.scalars(statement).one()

            _ = db_object.user_admin

            return db_object

        except:
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

            session.merge(admin)

        except:
            session.rollback()
            return False

        else:
            session.commit()
            return True

def del_admin(user_id: int):
    with Session() as session:
        try:
            article = get_admin(user_id)
            session.delete(article)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True
