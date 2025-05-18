from sqlalchemy import select
from typing import List
from datetime import datetime

from .error_logs import add_errors
from error_logs import ErrorsBase
from .other import convert_dict_in_str
from users import UsersBase, ArticlesBase
from configurations import Session

def add_user(obj: UsersBase) -> UsersBase | bool:
    with Session() as session:
        try:
            session.add(obj)

            session.commit()
            session.refresh(obj)

            return obj

        except Exception as ex:
            session.rollback()  # Отменяет все незафиксированные изменения.

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - add_user(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_user(value: int | str, attribute: str = "none") -> UsersBase | None | bool:
    """
        Function to get user objects.

        Parameters:
            -  atribute - may be 'id' or 'login';
            -  value - sqarch value.

        Warning:
            If **attribute** == 'none' or other, then search will be **attribute** == 'id'.

    """

    with Session() as session:
        try:
            if attribute == "login":
                # Где выбрать и по какому полю.
                statement = select(UsersBase).where(UsersBase.login==value)
            else:
                statement = select(UsersBase).where(UsersBase.id==int(value))

            # Вернуть первый объект с типом python. all - вернет все объекты.
            db_object = session.scalars(statement).one_or_none()

            _ = db_object.article
            _ = db_object.admin
            _ = db_object.black_list
            _ = db_object.errors

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - get_user(value = {value}, attribute = {attribute})",
                error_date = datetime.now()
            ))

            return False

def update_user(id: int, **new_values) -> bool | None:
    """
        Function for updating user objects.

        Parameters:
            -  id - user ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """

    with Session() as session:
        try:
            user = get_user(id)
            if user != None:
                for key, value in new_values.items():
                    if hasattr(user, key) and value != None:  # Проверка на существование атрибута.
                        setattr(user, key, value)  # Изменение значения атрибута.

                # Проверяет есть ли в сессии объект с таким же ключем. В случае успеха обновляет его.
                session.merge(user)

                session.commit()
                return True
            else:
                return None

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - update_user(id = {id}, " +
                        f"**new_values = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

def del_user(id: int) -> bool | None:
    with Session() as session:
        try:
            user = get_user(id)
            if user != None:
                session.delete(user)

                session.commit()
                return True
            else:
                return None

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - del_user(id = {id})",
                error_date = datetime.now()
            ))

            return False

# ---------------------------------------------------- articles --------------------------------------------------

def add_article(obj: ArticlesBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)

            session.commit()
            return True
        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - add_article(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_article_by_id(id: int) -> ArticlesBase | None | bool:
    with Session() as session:
        try:
            statement = select(ArticlesBase).where(ArticlesBase.id==int(id))
            db_object = session.scalars(statement).one_or_none()

            _ = db_object.user

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - get_article_by_id(id = {id})",
                error_date = datetime.now()
            ))

            return False

def get_articles_by_user_id(user_id: int) -> List[ArticlesBase] | List | bool:
    with Session() as session:
        try:
            statement = select(ArticlesBase).where(ArticlesBase.user_id==int(user_id))

            db_object = session.scalars(statement).all()

            elem: ArticlesBase
            for elem in db_object:
                _ = elem.user

            return db_object

        except Exception as ex:

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - get_articles_by_user_id(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False

def update_article(id: int, **new_values) -> bool | None:
    """
        Function for updating user articles.

        Parameters:
            -  id - article ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """
    with Session() as session:
        try:
            article = get_article_by_id(id)
            if article != None:
                for key, value in new_values.items():
                    if hasattr(article, key) and value != None:
                        setattr(article, key, value)
            else:
                return None

            session.merge(article)

            session.commit()
            return True

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - update_article(id = {id}, " +
                        f"**new_values = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

def del_article(id: int) -> bool | None:
    with Session() as session:
        try:
            article = get_article_by_id(id)
            if article != None:
                session.delete(article)

                session.commit()
                return True
            else:
                return None

        except Exception as ex:
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - del_article(id = {id})",
                error_date = datetime.now()
            ))

            return False