from fastapi import APIRouter, status, HTTPException

from handler_logging import LokiLogginHandler
from black_list import BlackListBase
from . import table_models
import functions

import logging

black_list_api_logger = logging.getLogger(__name__)
black_list_api_logger.level = logging.DEBUG

black_list_api_file_handler = logging.FileHandler(f"logs/API/{__name__}.log", encoding="UTF-8")
black_list_api_file_handler_debug = logging.FileHandler(f"logs/API/{__name__}_debug.log", encoding="UTF-8")
black_list_api_file_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
black_list_api_file_loki_handler.level = logging.DEBUG
black_list_api_file_handler.level = logging.INFO
black_list_api_file_handler_debug.level = logging.DEBUG

black_list_api_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
black_list_api_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

black_list_api_file_handler.setFormatter(black_list_api_formatter)
black_list_api_file_handler_debug.setFormatter(black_list_api_formatter_debug)
black_list_api_file_loki_handler.setFormatter(black_list_api_formatter_debug)
black_list_api_logger.addHandler(black_list_api_file_handler)
black_list_api_logger.addHandler(black_list_api_file_handler_debug)
black_list_api_logger.addHandler(black_list_api_file_loki_handler)

black_list_router = APIRouter(prefix="/black_list", tags=["black_list"])

@black_list_router.post("/add/",
                     status_code=status.HTTP_201_CREATED,
                     summary="Adding user to blacklist",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}},
                     response_model=table_models.Response_model)
def add_black_list_api(black: table_models.Black_list_for_input_api):
    try:
        black_list_api_logger.info(f"Запрос на добавление в 'Black_list': user_id={black.id_user}")
        add = functions.add_black_list(BlackListBase(**black.__dict__))
        black_list_api_logger.info(f"Добавлен в 'black_list': user_id={black.id_user}")

        if add == False or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="sucesss",
            data=table_models.Black_list_api(**add.__dict__).__dict__
        )
    except HTTPException:
        black_list_api_logger.error(f"Произошла ошибка при добавлении в 'Black_list': user_id={black.id_user}",
                                    exc_info=True)
        raise
    except Exception as ex:
        black_list_api_logger.error(f"Произошла ошибка при добавлении в 'Black_list': user_id={black.id_user}",
                                    exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@black_list_router.get("/get/{id}",
                       status_code=status.HTTP_200_OK,
                       summary="Getting a user from the blacklist by id",
                       responses={400: {"description": "Invalid input data"},
                                  500: {"description": "Internal server error"}},
                       response_model=table_models.Response_model)
def get_black_list_id_api(id: int):
    try:
        black_list_api_logger.info(f"Запрос на получение из 'Black_list': id={id}")
        get = functions.get_user_black_list_id(id)
        black_list_api_logger.info(f"Получен из 'Black_list': id={id}")

        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Black_list_api(**get.__dict__).__dict__
        )
    except HTTPException:
        black_list_api_logger.error("Произошла ошибка при получении из 'Black_list': id={id}",
                                    exc_info=True)
        raise
    except Exception as ex:
        black_list_api_logger.error("Произошла ошибка при получении из 'Black_list': id={id}",
                                    exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@black_list_router.get("/get/user/{user_id}",
                       status_code=status.HTTP_200_OK,
                       summary="Getting a user from the blacklist by user id",
                       responses={400: {"description": "Invalid input data"},
                                  500: {"description": "Internal server error"}},
                       response_model=table_models.Response_model)
def get_black_list_user_id_api(user_id: int):
    try:
        black_list_api_logger.info(f"Запрос на получение из 'Black_list': user_id={user_id}")
        get = functions.get_user_black_list_user_id(user_id)
        black_list_api_logger.info(f"Получен из 'Black_list': user_id={user_id}")
        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Black_list_api(**get.__dict__).__dict__
        )
    except HTTPException:
        black_list_api_logger.error(f"Произошла ошибка при получении из 'Black_list': user_id={user_id}",
                                    exc_info=True)
        raise
    except Exception as ex:
        black_list_api_logger.error(f"Произошла ошибка при получении из 'Black_list': user_id={user_id}",
                                    exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@black_list_router.put("/put/{user_id}",
                       status_code=status.HTTP_200_OK,
                       summary="Update user blacklist by user id",
                       responses={400: {"description": "Invalid input data"},
                                  500: {"description": "Internal server error"}})
def update_user_black_list_api(user_id: int, black: table_models.Black_list_for_update_api):
    try:
        black_list_api_logger.info(f"Запрос на обновление в 'Black_list': user_id={user_id}")
        black_list_api_logger.debug(f"Запрос на обновление в 'Black_list': user_id={user_id}; {black.__dict__}")
        update = functions.update_user_black_list(user_id, **black.__dict__)
        black_list_api_logger.info(f"Обновлен в 'Black_list': user_id={user_id}")
        black_list_api_logger.debug(f"Обновлен в 'Black_list': user_id={user_id}; {black.__dict__}")

        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{update}"}

    except HTTPException:
        black_list_api_logger.error(f"Произошла ошибка при обновлении в 'Black_list': user_id={user_id}; {black.__dict__}",
                                    exc_info=True)
        raise
    except Exception as ex:
        black_list_api_logger.error(f"Произошла ошибка при обновлении в 'Black_list': user_id={user_id}; {black.__dict__}",
                                    exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@black_list_router.delete("/del/{user_id}",
                          status_code=status.HTTP_200_OK,
                          summary="Removing a user from the blacklist by user id",
                          responses={400: {"description": "Invalid input data"},
                                     500: {"description": "Internal server error"}})
def del_user_black_list_api(user_id: int):
    try:
        black_list_api_logger.info(f"Запрос на удалении из 'Black_list': user_id={user_id}")
        delete = functions.del_user_black_list(user_id)
        black_list_api_logger.info(f"Удален из 'Black_list': user_id={user_id}")

        if delete == False or delete is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{delete}"}

    except HTTPException:
        black_list_api_logger.error(f"Произошла ошибка при удалении из 'Black_list': user_id={user_id}",
                                    exc_info=True)
        raise
    except Exception as ex:
        black_list_api_logger.error(f"Произошла ошибка при удалении из 'Black_list': user_id={user_id}",
                                    exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )