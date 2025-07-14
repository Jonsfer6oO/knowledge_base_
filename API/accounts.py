from fastapi import APIRouter, status, HTTPException

from handler_logging import LokiLogginHandler
from accounts import AccountsBase
from . import table_models
import functions

import logging

accounts_api_logger = logging.getLogger(__name__)
accounts_api_logger.setLevel(logging.DEBUG)

accounts_api_file_handler = logging.FileHandler(f"logs/API/{__name__}.log", encoding="UTF-8")
accounts_api_file_handler_debug = logging.FileHandler(f"logs/API/{__name__}_debug.log", encoding="UTF-8")
accounts_api_file_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
accounts_api_file_loki_handler.level = logging.DEBUG
accounts_api_file_handler.level = logging.INFO
accounts_api_file_handler_debug.level = logging.DEBUG
accounts_api_formmater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
accounts_api_formmater_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

accounts_api_file_handler.setFormatter(accounts_api_formmater)
accounts_api_file_handler_debug.setFormatter(accounts_api_formmater_debug)
accounts_api_file_loki_handler.setFormatter(accounts_api_formmater_debug)
accounts_api_logger.addHandler(accounts_api_file_handler)
accounts_api_logger.addHandler(accounts_api_file_handler_debug)
accounts_api_logger.addHandler(accounts_api_file_loki_handler)

account_router = APIRouter(prefix="/accounts", tags=["accounts"])

@account_router.post("/add/",
                     status_code=status.HTTP_201_CREATED,
                     summary="Adds account data to the database",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}},
                     response_model=table_models.Response_model)
def add_account_api(account: table_models.Account_for_input_api):
    try:
        accounts_api_logger.info(f"Запрос на добавление в 'Accounts': id={account.login}")
        add = functions.add_account(AccountsBase(**account.__dict__))
        accounts_api_logger.info(f"Записан в базу 'Accounts': login={account.login}")

        if add == False or add is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type = "success",
            data = table_models.Account_api(**add.__dict__).__dict__
        )
    except HTTPException:
        accounts_api_logger.error(f"Произошла ошибка при записи в 'Accounts': login={account.login}",
                                  exc_info=True)
        raise
    except Exception as ex:
        accounts_api_logger.error(f"Произошла ошибка при записи в 'Accounts': login={account.login}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@account_router.get("/get/{value}",
                    status_code=status.HTTP_200_OK,
                    summary="Getting an account from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def get_account_api(value: int | str, attribute="none"):
    try:
        accounts_api_logger.info(f"Запрос на поулчение из 'Accounts': value={value}; attribute={attribute}")
        get = functions.get_account(value, attribute)
        accounts_api_logger.info(f"Получен из 'Accounts': value={value}; attribute={attribute}")

        if get == False or get is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type = "success",
            data = table_models.Account_api(**get.__dict__).__dict__
        )
    except HTTPException:
        accounts_api_logger.error(f"Произошла ошибка при получении из 'Accounts': value={value}",
                                  exc_info=True)
        raise
    except Exception as ex:
        accounts_api_logger.error(f"Произошла ошибка при получении из 'Accounts': value={value}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@account_router.put("/put/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Account updates from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def update_account_api(id: int, account: table_models.Account_for_update_api):
    try:
        accounts_api_logger.info(f"Запрос на обновление в 'Accounts': id={id}")
        accounts_api_logger.debug(f"Запрос на обновление в 'Accounts': id={id}; {account.__dict__}")
        update = functions.update_account(id, **account.__dict__)
        accounts_api_logger.info(f"Обновлен в 'Accounts': id={id}")
        accounts_api_logger.debug(f"Обновлен в 'Accounts': id={id}; {account.__dict__}")

        if update == False or update is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{update}"}
    except HTTPException:
        accounts_api_logger.error(f"Произошла ошибка при обновлении в 'Accounts': id={id}; {account.__dict__}",
                                  exc_info=True)
        raise
    except Exception as ex:
        accounts_api_logger.error(f"Произошла ошибка при обновлении в 'Accounts': id={id}; {account.__dict__}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@account_router.delete("/del/{id}",
                       status_code=status.HTTP_200_OK,
                       summary="Removing an account from the database",
                       responses={400: {"description": "Invalid input data"},
                                  500: {"description": "Internal server error"}})
def del_account_api(id: int):
    try:
        accounts_api_logger.info(f"Запрос на удаление из 'Accounts': id={id}")
        delete = functions.del_account(id)
        accounts_api_logger.info(f"Удален из 'Accounts': id={id}")

        if delete == False or delete is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )
        return {"type": "success", "status": f"{delete}"}
    except HTTPException:
        accounts_api_logger.error(f"Произошла ошибка при удалении из 'Accounts': id={id}",
                                  exc_info=True)
        raise
    except Exception as ex:
        accounts_api_logger.error(f"Произошла ошибка при удалении из 'Accounts': id={id}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )