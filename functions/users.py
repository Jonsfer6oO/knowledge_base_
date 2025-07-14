from sqlalchemy import select
from typing import List
from datetime import datetime

from handler_logging import LokiLogginHandler
from .error_logs import add_errors
from error_logs import ErrorsBase
from .other import convert_dict_in_str
from users import UsersBase, ArticlesBase
from configurations import Session

import logging

users_functions_logger = logging.getLogger(__name__)
users_functions_logger.setLevel(logging.DEBUG)

users_functions_handler = logging.FileHandler(f"logs/functions/{__name__}.log", encoding="UTF-8")
users_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_debug.log", encoding="UTF-8")
users_functions_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
users_functions_loki_handler.level = logging.DEBUG
users_functions_handler.level = logging.INFO
users_functions_handler_debug.level = logging.DEBUG
users_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
users_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

users_functions_handler.setFormatter(users_functions_formatter)
users_functions_handler_debug.setFormatter(users_functions_formatter_debug)
users_functions_loki_handler.setFormatter(users_functions_formatter_debug)
users_functions_logger.addHandler(users_functions_handler)
users_functions_logger.addHandler(users_functions_handler_debug)
users_functions_logger.addHandler(users_functions_loki_handler)

articles_functions_logger = logging.getLogger(f"{__name__}_artciles")
articles_functions_logger.setLevel(logging.DEBUG)

articles_functions_handler = logging.FileHandler(f"logs/functions/{__name__}_articles.log", encoding="UTF-8")
articles_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_articles_debug.log", encoding="UTF-8")
articles_functions_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
articles_functions_loki_handler.level = logging.DEBUG
articles_functions_handler.level = logging.INFO
articles_functions_handler_debug.level = logging.DEBUG
articles_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
articles_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

articles_functions_handler.setFormatter(articles_functions_formatter)
articles_functions_handler_debug.setFormatter(articles_functions_formatter_debug)
articles_functions_loki_handler.setFormatter(articles_functions_formatter_debug)
articles_functions_logger.addHandler(articles_functions_handler)
articles_functions_logger.addHandler(articles_functions_handler_debug)
articles_functions_logger.addHandler(articles_functions_loki_handler)

def add_user(obj: UsersBase) -> UsersBase | bool:
    users_functions_logger.info(f"Запрос на добавление в 'Users': login={obj.login}")
    with Session() as session:
        try:
            session.add(obj)
            users_functions_logger.info(f"Добавление объекта в сессию 'Users': login={obj.login}")

            session.commit()
            users_functions_logger.info(f"Коммит изменений в 'Users': login={obj.login}")
            session.refresh(obj)
            users_functions_logger.debug(f"{obj.__dict__}")

            return obj

        except Exception as ex:
            users_functions_logger.error(f"Ошибка при добавлении в 'Users': login={obj.login}",
                                         exc_info=True)
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

    users_functions_logger.info(f"Запрос на получение из 'Users': value={value}; attribute={attribute}")
    with Session() as session:
        try:
            if attribute == "login":
                # Где выбрать и по какому полю.
                statement = select(UsersBase).where(UsersBase.login==value)
                users_functions_logger.info(f"Создан запрос на выбор данных по login из 'Users': value={value}; attribute={attribute}")
            else:
                statement = select(UsersBase).where(UsersBase.id==int(value))
                users_functions_logger.info(f"Создан запрос на выбор данных по id из 'Users': value={value}; attribute={attribute}")

            # Вернуть первый объект с типом python. all - вернет все объекты.
            db_object = session.scalars(statement).one_or_none()
            users_functions_logger.info(f"Данные из 'Users' получены: value={value}; attribute={attribute}")
            users_functions_logger.debug(f"{db_object.__dict__}")

            _ = db_object.article
            _ = db_object.admin
            _ = db_object.black_list
            _ = db_object.errors

            return db_object

        except Exception as ex:
            users_functions_logger.error(f"Ошибка при полчении из 'Users': value={value}; attribute={attribute}",
                                         exc_info=True)
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

    users_functions_logger.info(f"Запрос на обновление в 'Users': id={id}")
    with Session() as session:
        try:
            user = get_user(id)
            users_functions_logger.info(f"Данные из 'Users' полученны: id={id}")
            if user != None and type(user) != bool:
                users_functions_logger.debug(f"{user.__dict__}")
                users_functions_logger.info(f"Начало обновления в 'Users': id={id}")
                for key, value in new_values.items():
                    if hasattr(user, key) and value != None:  # Проверка на существование атрибута.
                        setattr(user, key, value)  # Изменение значения атрибута.
                users_functions_logger.info(f"Конец обновления в 'Users': id={id}; {new_values}")
                users_functions_logger.debug(f"{user.__dict__}")
                # Проверяет есть ли в сессии объект с таким же ключем. В случае успеха обновляет его.
                session.merge(user)
                users_functions_logger.info(f"Слияние жанных с данными в сессии 'Users': id={id}")

                session.commit()
                users_functions_logger.info(f"Комиит изменений в 'Users': id={id}")
                return True
            else:
                users_functions_logger.info(f"Данные в 'Users' не найдены: id={id}")
                return None

        except Exception as ex:
            users_functions_logger.error(f"Ошибка при обновлении данных в 'Users': id={id}",
                                         exc_info=True)
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
    users_functions_logger.info(f"Запрос на удалении из 'Users': id={id}")
    with Session() as session:
        try:
            user = get_user(id)
            users_functions_logger.info(f"Данные из 'Users' полученны: id={id}")
            if user != None and type(user) != bool:
                users_functions_logger.debug(f"{user.__dict__}")
                session.delete(user)
                users_functions_logger.info(f"Удаление данных из сессии 'Users': id={id}")

                session.commit()
                users_functions_logger.info(f"Коммит измнений в 'Users': id={id}")
                return True
            else:
                return None

        except Exception as ex:
            users_functions_logger.error(f"Ошибка при удалени из 'Users': id={id}",
                                         exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - del_user(id = {id})",
                error_date = datetime.now()
            ))

            return False

# ---------------------------------------------------- articles --------------------------------------------------

def add_article(obj: ArticlesBase) -> ArticlesBase | bool:
    articles_functions_logger.info(f"Запрос на добавление в 'Artciles': user_id={obj.user_id}; title={obj.title}")
    with Session() as session:
        try:
            session.add(obj)
            articles_functions_logger.info(f"Доавбление данных в сессию 'Artciles': user_id={obj.user_id}; title={obj.title}")

            session.commit()
            articles_functions_logger.info(f"Коммит изменений в 'Artciels': user_id={obj.user_id}; title={obj.title}")
            session.refresh(obj)
            articles_functions_logger.debug(f"{obj.__dict__}")

            return obj
        except Exception as ex:
            articles_functions_logger.error(f"Ошибка при добавлении в 'Articles': user_id={obj.user_id}; title={obj.title}",
                                            exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - add_article(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_article_by_id(id: int) -> ArticlesBase | None | bool:
    articles_functions_logger.info(f"Запрос на поулчение из 'Artciels' по id: id={id}")
    with Session() as session:
        try:
            statement = select(ArticlesBase).where(ArticlesBase.id==int(id))
            articles_functions_logger.info(f"Создан запрос на выбор данных по id из 'Artciels': id={id}")
            db_object = session.scalars(statement).one_or_none()
            articles_functions_logger.info(f"Данные из 'Articles' полученны: id={id}")
            articles_functions_logger.debug(f"{db_object.__dict__}")

            _ = db_object.user

            return db_object

        except Exception as ex:
            articles_functions_logger.error(f"Ошибка при получении данных по id из 'Articles': id={id}",
                                            exc_info=True)
            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - get_article_by_id(id = {id})",
                error_date = datetime.now()
            ))

            return False

def get_articles_by_user_id(user_id: int) -> List[ArticlesBase] | List | bool:
    articles_functions_logger.info(f"Запрос на поулчение данных из 'Articles' по user_id: user_id={user_id}")
    with Session() as session:
        try:
            statement = select(ArticlesBase).where(ArticlesBase.user_id==int(user_id))
            articles_functions_logger.info(f"Создан запрос на выбор данных по user_id из 'Articles': user_id={user_id}")

            db_object = session.scalars(statement).all()
            articles_functions_logger.info(f"Данные из 'Articles' полученны: user_id={user_id}")

            elem: ArticlesBase
            for elem in db_object:
                _ = elem.user

            return db_object

        except Exception as ex:
            articles_functions_logger.error(f"Ошибка при получении данных из 'Articles' по user_id: user_id={user_id}",
                                            exc_info=True)
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

    articles_functions_logger.info(f"Запрос на обновление данных в 'Articles': id={id}")
    with Session() as session:
        try:
            article = get_article_by_id(id)
            articles_functions_logger.info(f"Данные из 'Artciles' полученны: id={id}")
            if article != None and type(article) != bool:
                articles_functions_logger.debug(f"{article.__dict__}")
                articles_functions_logger.info(f"Начало обновления данных в 'Artciels': id={id}")
                for key, value in new_values.items():
                    if key == "text" and value != None:
                        value = bytes(value, "utf-8")
                    if hasattr(article, key) and value != None:
                        setattr(article, key, value)
                articles_functions_logger.info(f"Конец обновления данных в 'Articles': id={id}")
            else:
                articles_functions_logger.info(f"Данные в 'Artciels' не найдены: id={id}")
                return None

            session.merge(article)
            articles_functions_logger.info(f"Слияние данных с данными в сессии 'Articles': id={id}")

            session.commit()
            articles_functions_logger.info(f"Коммит данных в 'Artciels': id={id}")
            return True

        except Exception as ex:
            articles_functions_logger.error(f"Ошибка при обновлении данных в 'Articles': id={id}; {new_values}",
                                            exc_info=True)
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
    articles_functions_logger.info(f"Запрос на удалении из 'Articels': id={id}")
    with Session() as session:
        try:
            article = get_article_by_id(id)
            articles_functions_logger.info(f"Данные из 'Artciels' полученны: id={id}")
            if article != None and type(article) != bool:
                articles_functions_logger.debug(f"{article.__dict__}")
                session.delete(article)
                articles_functions_logger.info(f"Данные в сессии 'Artciels' удалены: id={id}")

                session.commit()
                articles_functions_logger.info(f"Комиит данных в 'Articles': id={id}")
                return True
            else:
                articles_functions_logger.info(f"Данные в 'Articles' не найдены: id={id}")
                return None

        except Exception as ex:
            articles_functions_logger.error(f"Ошибка при удалении данных из 'Articles': id={id}",
                                            exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/users.py] - del_article(id = {id})",
                error_date = datetime.now()
            ))

            return False