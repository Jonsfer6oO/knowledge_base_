from sqlalchemy import select
from datetime import datetime

from black_list import BlackListBase
from configurations import Session
from .error_logs import add_errors
from error_logs import ErrorsBase
from .other import convert_dict_in_str

import logging

black_list_functions_logger = logging.getLogger(__name__)
black_list_functions_logger.setLevel(logging.DEBUG)

black_list_functions_handler = logging.FileHandler(f"logs/functions/{__name__}.log", encoding="UTF-8")
black_list_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_debug.log", encoding="UTF-8")
black_list_functions_handler.level = logging.INFO
black_list_functions_handler_debug.level = logging.DEBUG
black_list_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
black_list_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

black_list_functions_handler.setFormatter(black_list_functions_formatter)
black_list_functions_handler_debug.setFormatter(black_list_functions_formatter_debug)
black_list_functions_logger.addHandler(black_list_functions_handler)
black_list_functions_logger.addHandler(black_list_functions_handler_debug)

def add_black_list(obj: BlackListBase) -> BlackListBase | bool:
    black_list_functions_logger.info(f"Запрос на добавление в 'Black_list': user_id={obj.id_user}")
    with Session() as session:
        try:
            session.add(obj)
            black_list_functions_logger.info(f"Добавление объекта в сессию 'Black_list': user_id={obj.id_user}")

            session.commit()
            black_list_functions_logger.info(f"Коммит измнений в 'Black_list': user_id={obj.id_user}")
            session.refresh(obj)
            black_list_functions_logger.debug(f"{obj.__dict__}")

            return obj

        except Exception as ex:
            black_list_functions_logger.error(f"Ошибка при записи в 'Black_list': user_id={obj.id_user}",
                                              exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - add_black_list(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_user_black_list_id(id: int) -> BlackListBase | None | bool:
    black_list_functions_logger.info(f"Запрос на получение из 'Black_list': id={id}")
    with Session() as session:
        try:
            statement = select(BlackListBase).where(BlackListBase.id==int(id))
            black_list_functions_logger.info(f"Создан запрос на выбор данных по id: id={id}")
            db_object = session.scalars(statement).one_or_none()
            black_list_functions_logger.info(f"Данные из 'Black_list' поулучены: id={id}")
            black_list_functions_logger.debug(f"{db_object.__dict__}")

            _ = db_object.user_black

            return db_object

        except Exception as ex:
            black_list_functions_logger.error(f"Ошибка при получении из 'Black_list' по id: id={id}",
                                              exc_info=True)
            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - get_user_black_list_id(id = {id})",
                error_date = datetime.now()
            ))

            return False

def get_user_black_list_user_id(user_id: int) -> BlackListBase | None | bool:
    black_list_functions_logger.info(f"Запрос на получение из 'Black_list' по user_id: user_id={user_id}")
    with Session() as session:
        try:
            statement = select(BlackListBase).where(BlackListBase.id_user==int(user_id))
            black_list_functions_logger.info(f"Создан запрос на выбор данных из 'Black_list' по user_id: user_id={user_id}")
            db_object = session.scalars(statement).one_or_none()
            black_list_functions_logger.info(f"Данные из 'Black_list' по user_id полученны: user_id={user_id}")
            black_list_functions_logger.debug(f"{db_object.__dict__}")

            _ = db_object.user_black

            return db_object

        except Exception as ex:
            black_list_functions_logger.error(f"Ошибка при получении из 'Black_list' по user_id: user_id={user_id}",
                                              exc_info=True)
            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - get_user_black_list_user_id(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False

def update_user_black_list(user_id: int, **new_values) -> bool | None:
    """
        Function for updating user in black list.

        Parameters:
            -  id - user ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """

    black_list_functions_logger.info(f"Запрос на обновление в 'Black_list': user_id={user_id}")
    with Session() as session:
        try:
            user_black_list = get_user_black_list_user_id(user_id)
            black_list_functions_logger.info(f"Полученны данные из 'Black_list': user_id={user_id}")
            if user_black_list != None and type(user_black_list) != bool:
                black_list_functions_logger.debug(f"{user_black_list.__dict__}")
                black_list_functions_logger.info(f"Начало обновления в 'Black_list': user_id={user_id}")
                for key, value in new_values.items():
                    if hasattr(user_black_list, key) and value != None:
                        setattr(user_black_list, key, value)
                black_list_functions_logger.info(f"Конец обновления в 'Black_list': user_id={user_id}")
                black_list_functions_logger.debug(f"{user_black_list.__dict__}")
            else:
                black_list_functions_logger.info(f"Строка в 'Black_list' не найдена: user_id={user_id}")
                return None

            session.merge(user_black_list)
            black_list_functions_logger.info(f"Слияние данных с данными в сессии 'Black_list': user_id={user_id}")

            session.commit()
            black_list_functions_logger.info(f"Коммит данных в 'Black_list': user_id={user_id}")
            return True

        except Exception as ex:
            black_list_functions_logger.error(f"Ошибка при обновлени в 'Black_list': user_id={user_id}",
                                              exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - update_user_black_list(user_id = {user_id}, " +
                        f"**new_values = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

def del_user_black_list(user_id: int) -> bool | None:
    black_list_functions_logger.info(f"Запрос на удалении из 'Black_list': user_id={user_id}")
    with Session() as session:
        try:
            user_black_list = get_user_black_list_user_id(user_id)
            black_list_functions_logger.info(f"Данные из 'Black_list' полученны: user_id={user_id}")
            if user_black_list != None and type(user_black_list) != bool:
                session.delete(user_black_list)
                black_list_functions_logger.info(f"Данные в сессии 'Black_list' удалены: user_id={user_id}")

                session.commit()
                black_list_functions_logger.info(f"Коммит в 'Black_list': user_id={user_id}")
                return True
            else:
                black_list_functions_logger.info(f"Данные в 'Black_list' не найдены: user_id={user_id}")
                return None

        except Exception as ex:
            black_list_functions_logger.error(f"Ошибка при удалении из 'Black_list': user_id={user_id}",
                                              exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/black_list.py] - del_user_black_list(user_id = {user_id})",
                error_date = datetime.now()
            ))

            return False