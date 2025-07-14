from sqlalchemy import select
from typing import List
from datetime import datetime

from handler_logging import LokiLogginHandler
from admins import AdminsBase
from configurations import Session
from crypto import hashed_password
from .other import convert_dict_in_str
from error_logs import ErrorsBase
from .error_logs import add_errors

import logging

admins_functions_logger = logging.getLogger(__name__)
admins_functions_logger.setLevel(logging.DEBUG)

admins_functions_handler = logging.FileHandler(f"logs/functions/{__name__}.log", encoding="UTF-8")
admins_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_debug.log", encoding="UTF-8")
admins_functions_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
admins_functions_loki_handler.level = logging.DEBUG
admins_functions_handler.level = logging.INFO
admins_functions_handler_debug.level = logging.DEBUG
admins_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
admins_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

admins_functions_handler.setFormatter(admins_functions_formatter)
admins_functions_handler_debug.setFormatter(admins_functions_formatter_debug)
admins_functions_loki_handler.setFormatter(admins_functions_formatter_debug)
admins_functions_logger.addHandler(admins_functions_handler)
admins_functions_logger.addHandler(admins_functions_handler_debug)
admins_functions_logger.addHandler(admins_functions_loki_handler)

def add_admin(obj: AdminsBase) -> AdminsBase | bool:
    admins_functions_logger.info(f"Запрос на добавление в 'Admins': login={obj.login}")
    with Session() as session:
        try:
            session.add(obj)
            admins_functions_logger.info(f"Добавление объекта в сессию 'Admins': login={obj.login}")

            session.commit()
            admins_functions_logger.info(f"Коммит изменений в 'Admins': login={obj.login}")
            session.refresh(obj)
            admins_functions_logger.debug(f"{obj}")

            return obj

        except Exception as ex:
            admins_functions_logger.error(f"Ошибка при добавлении в 'Admins': {obj.__dict__}",
                                          exc_info=True)
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

    admins_functions_logger.info(f"Запрос на получение из 'Admins': value={value}; attribute={attribute}")
    with Session() as session:
        try:
            if attribute == "login":
                statement = select(AdminsBase).where(AdminsBase.login==value)
                admins_functions_logger.info(f"Создан запрос на выбор по login: value={value}; attribute={attribute}")
            else:
                statement = select(AdminsBase).where(AdminsBase.id_user==int(value))
                admins_functions_logger.info(f"Создан запрос на выбор по user_id: value={value}; attribute={attribute}")

            db_object = session.scalars(statement).one_or_none()
            admins_functions_logger.info(f"Данные из 'Admins' полученны: value={value}; attribute={attribute}")
            admins_functions_logger.debug(f"{db_object}")

            _ = db_object.user_admin

            return db_object

        except Exception as ex:
            admins_functions_logger.error(f"Ошибка при получении из 'Admins': value={value}; attribute={attribute}",
                                          exc_info=True)
            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - get_admin(value = {value}, attribute = {attribute})",
                error_date = datetime.now()
            ))

            return False

def get_admin_by_id(id: int) -> AdminsBase | None | bool:
    admins_functions_logger.info(f"Запрос на получение данных по id из 'Admins': id={id}")
    with Session() as session:
        try:
            statement = select(AdminsBase).where(AdminsBase.id==int(id))
            admins_functions_logger.info(f"Создан запрос на выбор данных по id из 'Admins': id={id}")
            db_object = session.scalars(statement).one_or_none()
            admins_functions_logger.info(f"Данные из 'Admins' полученны: id={id}")
            admins_functions_logger.debug(f"{db_object}")

            _ = db_object.user_admin

            return db_object

        except Exception as ex:
            admins_functions_logger.error(f"Ошибка при получении данных по user_id: id={id}",
                                           exc_info=True)

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

    admins_functions_logger.info(f"Запрос на обновление в 'Admins': user_id={user_id}")
    with Session() as session:
        try:
            admin = get_admin(user_id)
            admins_functions_logger.info(f"Данные из 'Admins' получены: user_id={user_id}")
            if admin != None and type(admin) != bool:
                admins_functions_logger.debug(f"{admin.__dict__}")
                admins_functions_logger.info(f"Начало обновления данных в 'Admins': user_id={user_id}")
                for key, value in new_values.items():
                    if hasattr(admin, key) and value != None:
                        setattr(admin, key, value)

                    if new_values.get("password") != None:
                        salt, hash_pass = hashed_password(new_values["password"])

                        admin.salt = salt
                        admin.password = hash_pass
                admins_functions_logger.info(f"Конец обновления в 'Admins': user_id={user_id}")
            else:
                admins_functions_logger.info(f"Данные в 'Admins' не найдены: user_id={user_id}")
                return None

            session.merge(admin)
            admins_functions_logger.info(f"Слияние данных с данными в сессии 'Admins': user_id={user_id}")
            admins_functions_logger.info(f"{admin.__dict__}")

            session.commit()
            admins_functions_logger.info(f"Коммит данных в 'Accounts': user_id={user_id}")
            return True

        except Exception as ex:
            admins_functions_logger.error(f"Ошибка при обновлении в 'Admins': user_id={user_id}",
                                          exc_info=True)
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
    admins_functions_logger.info(f"Запрос на удаление из 'Admins': user_id={user_id}")
    with Session() as session:
        try:
            admin = get_admin(user_id)
            admins_functions_logger.info(f"Данные из 'Admins' полученны: user_id={user_id}")
            if admin != None and type(admin) != bool:
                session.delete(admin)
                admins_functions_logger.info(f"Данные в сессии 'Accounts' удалены: user_id={user_id}")

                session.commit()
                admins_functions_logger.info(f"Коммит изменений в 'Admins': user_id={user_id}")
                return True

            else:
                admins_functions_logger.info(f"Данные в 'Admins' не найдены: user_id={user_id}")
                return None

        except Exception as ex:
            admins_functions_logger.error(f"Ошибка при удалении из 'Admins': user_id={user_id}",
                                          exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/admins.py] - del_admin(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False
