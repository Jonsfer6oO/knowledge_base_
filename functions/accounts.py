import logging.handlers
from sqlalchemy import select
from typing import List
from datetime import datetime

from accounts import AccountsBase
from configurations import Session
from crypto import hashed_password
from .other import convert_dict_in_str
from error_logs import ErrorsBase
from .error_logs import add_errors

import logging

accounts_functions_logger = logging.getLogger(__name__)
accounts_functions_logger.setLevel(logging.DEBUG)

accounts_functions_handler = logging.FileHandler(f"logs/functions/{__name__}.log", encoding="UTF-8")
accounts_functions_handler_debug = logging.FileHandler(f"logs/functions/{__name__}_debug.log", encoding="UTF-8")
accounts_functions_handler.level = logging.INFO
accounts_functions_handler_debug.level = logging.DEBUG
accounts_functions_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
accounts_functions_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

accounts_functions_handler.setFormatter(accounts_functions_formatter)
accounts_functions_handler_debug.setFormatter(accounts_functions_formatter_debug)
accounts_functions_logger.addHandler(accounts_functions_handler)
accounts_functions_logger.addHandler(accounts_functions_handler_debug)

def add_account(obj: AccountsBase) -> AccountsBase | bool:
    accounts_functions_logger.info(f"Запрос на добавление в 'Accounts': login={obj.login}")
    with Session() as session:
        try:
            session.add(obj)
            accounts_functions_logger.info(f"Добавление объекта в сессию 'Accounts': login={obj.login}")

            session.commit()
            accounts_functions_logger.info(f"Коммит изменний в 'Accounts': login={obj.login}")
            session.refresh(obj)
            accounts_functions_logger.debug(f"{obj.__dict__}")

            return obj

        except Exception as ex:
            accounts_functions_logger.error(f"Ошибка при добавлении в 'Accounts': {obj.__dict__}",
                                            exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - add_account(obj = {obj})",
                error_date = datetime.now()
            ))

            return False

def get_account(value: int | str, attribute: str = "none") -> AccountsBase | None | bool:
    """
        Function to get account objects.

        Parameters:
            -  atribute - may be 'id' or 'login';
            -  value - sqarch value.

        Warning:
            If **attribute** == 'none' or other, then search will be **attribute** == 'id'.

    """

    accounts_functions_logger.info(f"Запрос на получение из 'Accounts': value={value}; attribute={attribute}")
    with Session() as session:
        try:
            if attribute == "login":
                statement = select(AccountsBase).where(AccountsBase.login==value)
                accounts_functions_logger.info(f"Создан запрос на выбор данных по login из 'Accounts': value={value}; attribute={attribute}")
            else:
                statement = select(AccountsBase).where(AccountsBase.id==int(value))
                accounts_functions_logger.info(f"Создан запрос на выбор данных по id из 'Accounts': value={value}; attribute={attribute}")

            db_object = session.scalars(statement).one_or_none()
            accounts_functions_logger.info(f"Данные из 'Accounts' получены: value={value}; attribute={attribute}")
            accounts_functions_logger.debug(f"{db_object}")

            return db_object

        except Exception as ex:
            accounts_functions_logger.error(f"Ошибка при получении данных из 'Accounts': value={value}; attribute={attribute}",
                                            exc_info=True)

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - get_account(value = {value}, attribute = {attribute})",
                error_date = datetime.now()
            ))

            return False

def update_account(id: int, **new_values) -> bool | None:
    """
        Function for updating admin.

        Parameters:
            -  id - account ID;
            -  new_values - key: attribute class, value: new value.

        Warning:
            If you pass non-existent attribute, they will be missed.
    """
    accounts_functions_logger.info(f"Запрос на обновление в 'Accounts': id={id}")
    with Session() as session:
        try:
            account = get_account(id)
            accounts_functions_logger.info(f"Получены данные из 'Accounts': id={id}")

            if account != None and type(account) != bool:
                accounts_functions_logger.debug(f"{account.__dict__}")
                accounts_functions_logger.info(f"Начало обновления в 'Accounts': id={id}")
                for key, value in new_values.items():
                    if hasattr(account, key) and value != None:
                        setattr(account, key, value)

                    if new_values.get("password") != None:
                        salt, hash_pass = hashed_password(new_values["password"])

                        account.salt = salt
                        account.password = hash_pass
                accounts_functions_logger.info(f"Конец обновления в 'Accounts': id={id}")
                accounts_functions_logger.debug(f"{account.__dict__}")
            else:
                accounts_functions_logger.info(f"Строка в 'Accounts' не найдена: id={id}")
                return None


            session.merge(account)
            accounts_functions_logger.info(f"Слияние данных с данными в сессии 'Accounts': id={id}")

            session.commit()
            accounts_functions_logger.info(f"Коммит данных в 'Accounts': id={id}")
            return True

        except Exception as ex:
            accounts_functions_logger.error(f"Ошибка при обновлении в 'Accounts': id={id}",
                                            exc_info=True)
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - update_account(id = {id}, " +
                        f"**new_value = {convert_dict_in_str(new_values)})",
                error_date = datetime.now()
            ))

            return False

def del_account(id: int) -> bool | None:
    accounts_functions_logger.info(f"Запрос на удаление из 'Accounts': id={id}")
    with Session() as session:
        try:
            account = get_account(id)
            accounts_functions_logger.info(f"Данные из 'Accounts' полученны: id={id}")
            if account != None and type(account) != bool:
                accounts_functions_logger.debug(f"{account}")
                session.delete(account)
                accounts_functions_logger.info(f"Данные в сессии 'Accounts' удалены: id={id}")

                session.commit()
                accounts_functions_logger.info(f"Коммит изменений в 'Accounts': id={id}")
                return True
            else:
                accounts_functions_logger.info(f"Данные в 'Accounts' не найдены: id={id}")
                return None

        except Exception as ex:
            accounts_functions_logger.error(f"Ошибка при удалении из 'Accounts': id={id}")
            session.rollback()

            add_errors(ErrorsBase(
                id_user = 0,
                message = str(ex),
                event = f"[functions/accounts.py] - del_account(id = {id})",
                error_date = datetime.now()
            ))

            return False