from fastapi import APIRouter, status, HTTPException

from handler_logging import LokiLogginHandler
from users import UsersBase
from . import table_models
import functions

import logging

users_api_logger = logging.getLogger(__name__)
users_api_logger.setLevel(logging.DEBUG)

users_api_file_handler = logging.FileHandler(filename=f"logs/API/{__name__}.log", encoding="UTF-8")
users_api_file_handler.level = logging.INFO
users_api_file_handler_debug = logging.FileHandler(filename=f"logs/API/{__name__}_debug.log", encoding="UTF-8")
users_api_file_handler_debug.level = logging.DEBUG
user_api_file_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
user_api_file_loki_handler.level = logging.DEBUG
users_api_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
users_api_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

users_api_file_handler.setFormatter(users_api_formatter)
users_api_file_handler_debug.setFormatter(users_api_formatter_debug)
user_api_file_loki_handler.setFormatter(users_api_formatter_debug)
users_api_logger.addHandler(users_api_file_handler)
users_api_logger.addHandler(users_api_file_handler_debug)
users_api_logger.addHandler(user_api_file_loki_handler)

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/add/",
                  status_code=status.HTTP_201_CREATED,
                  summary="Adds a new user to the database",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def add_users_api(user: table_models.User_for_input_api):
    try:
        users_api_logger.info(f"Добавление в 'Users': login={user.login}")
        adding = functions.add_user(UsersBase(**user.__dict__))
        users_api_logger.info(f"Добавлен в 'Users': login={user.login}.")

        if adding == False or adding is None :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User regestration failed"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.User_api(**adding.__dict__).__dict__)
    except HTTPException:
        users_api_logger.error(f"Произошла ошибка при записи 'Users'", exc_info=True)
        raise
    except Exception as ex:
        users_api_logger.error(f"Произошла ошибка при записи 'Users'", exc_info=True)
        # Неизвестная ошибка со стороны сервера
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@user_router.get("/get/{value}",
                 status_code=status.HTTP_200_OK,
                 summary="Getting user from database",
                 responses={400: {"description": "Invalid input data"},
                            500: {"description": "Internal server error"}},
                 response_model=table_models.Response_model)
def get_users_api(value: int | str, attribute: str="none"):
    try:
        users_api_logger.info(f"Запрос на получение из 'Users': value={value}; attribute={attribute}")
        get = functions.get_user(value=value, attribute=attribute)
        users_api_logger.info(f"Получен из 'Users': value={value}; attribute={attribute}")

        if get == False or get is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.User_api(**get.__dict__).__dict__
        )
    except HTTPException:
        users_api_logger.error(f"Произошла ошибка при получени 'Users': value={value}; attribute={attribute}",
                               exc_info=True)
        raise
    except Exception as ex:
        users_api_logger.error(f"Произошла ошибка при получени 'Users': value={value}; attribute={attribute}",
                               exc_info=True)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@user_router.put("/put/{id}",
                 status_code=status.HTTP_200_OK,
                 summary="Updating a user in the database",
                 responses={400: {"description": "Invalid input data"},
                            500: {"description": "Internal server error"}})
def update_users_api(id: int, user: table_models.User_for_update_api):
    try:
        users_api_logger.info(f"Обновление в 'Users': id={id}")
        users_api_logger.debug(f"Обновление в 'Users': id={id}; {user.__dict__}")
        update = functions.update_user(id, **user.__dict__)
        users_api_logger.info(f"Обновлен в 'Users': id={id}")
        users_api_logger.debug(f"Обновлен в 'Users': id={id}; {user.__dict__}")

        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{update}"}
    except HTTPException:
        users_api_logger.error(f"Произошла ошибка при обнолвении 'Users': id={id}; {user.__dict__}",
                               exc_info=True)
        raise
    except Exception as ex:
        users_api_logger.error(f"Произошла ошибка при обнолвении 'Users': id={id}; {user.__dict__}",
                               exc_info=True)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@user_router.delete("/del/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Removes a user from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def del_users_api(id: int):
    try:
        users_api_logger.info(f"Удаление из 'Users': id={id}")
        delete = functions.del_user(id)
        users_api_logger.info(f"Удален из 'Users': id={id}")

        if delete == False or delete is None:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{delete}"}
    except HTTPException:
        users_api_logger.info(f"Произошла ошибка при удалении из 'Users': id={id}")
        raise
    except Exception as ex:
        users_api_logger.info(f"Произошла ошибка при удалении из 'Users': id={id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )
