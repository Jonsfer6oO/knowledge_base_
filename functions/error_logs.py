from sqlalchemy import select
from typing import List

from error_logs import ErrorsBase
from configurations import Session

import logging

errors_functions_logger = logging.getLogger(__name__)
errors_functions_logger.setLevel(logging.DEBUG)

errors_functions_handler = logging.FileHandler(f"logs/functions/{__name__}.log", encoding="UTF-8")
errors_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_debug.log", encoding="UTF-8")
errors_functions_handler.level = logging.INFO
errors_functions_handler_debug.level = logging.DEBUG
errors_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
errors_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

errors_functions_handler.setFormatter(errors_functions_formatter)
errors_functions_handler_debug.setFormatter(errors_functions_formatter_debug)
errors_functions_logger.addHandler(errors_functions_handler)
errors_functions_logger.addHandler(errors_functions_handler_debug)

def add_errors(obj: ErrorsBase) -> ErrorsBase | bool:
    errors_functions_logger.info(f"Запрос на добавление в 'Errors': user_id={obj.id_user}")
    with Session() as session:
        try:
            session.add(obj)
            errors_functions_logger.info(f"Добавление объекта в сессию 'Errors': user_id={obj.id_user}")

            session.commit()
            errors_functions_logger.info(f"Коппит измнений в 'Errors': user_id={obj.id_user}")
            session.refresh(obj)
            errors_functions_logger.debug(f"{obj.__dict__}")

            return obj

        except:
            errors_functions_logger.error(f"Ошибка при записи в 'Errors': user_id={obj.id_user}",
                                          exc_info=True)
            session.rollback()
            return False

def get_error_by_id(id: int) -> ErrorsBase | None | bool:
    errors_functions_logger.info(f"Запрос на поулчение по id из 'Errors': id={id}")
    with Session() as session:
        try:
            statement = select(ErrorsBase).where(ErrorsBase.id==int(id))
            errors_functions_logger.info(f"Создан запрос на выбор по id из 'Errors': id={id}")
            db_object = session.scalars(statement).one_or_none()
            errors_functions_logger.info(f"Данные из 'Errors' получены: id={id}")
            errors_functions_logger.debug(f"{db_object.__dict__}")

            _ = db_object.user_errors

            return db_object

        except:
            errors_functions_logger.error(f"Ошибка при получении из 'Errors': id={id}",
                                          exc_info=True)
            return False

def get_errors_by_user_id(user_id: int) -> List[ErrorsBase] | List | bool:
    errors_functions_logger.info(f"Запрос на получение из 'Errors' по user_id: user_id={user_id}")
    with Session() as session:
        try:
            statement = select(ErrorsBase).where(ErrorsBase.id_user==int(user_id))
            errors_functions_logger.info(f"Создан запрос на выбор из 'Erros' по user_id: user_id={user_id}")

            db_object = session.scalars(statement).all()
            errors_functions_logger.info(f"Данные из 'Errors' полученны: user_id={user_id}")

            elem: ErrorsBase
            for elem in db_object:
                _ = elem.user_errors

            return db_object

        except:
            errors_functions_logger.error(f"Ошибка при получени из 'Errors' по user_id: user_id={user_id}",
                                          exc_info=True)
            return False