from fastapi import APIRouter, status, HTTPException

from admins import AdminsBase
from . import table_models
import functions

import logging

admins_api_logger = logging.getLogger(__name__)
admins_api_logger.level = logging.DEBUG

admins_api_file_handler = logging.FileHandler(f"logs/API/{__name__}.log", encoding="UTF-8")
admins_api_file_handler_debug = logging.FileHandler(f"logs/API/{__name__}_debug.log", encoding="UTF-8")
admins_api_file_handler.level = logging.INFO
admins_api_file_handler_debug.level = logging.DEBUG

admin_api_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
admin_api_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

admins_api_file_handler.setFormatter(admin_api_formatter)
admins_api_file_handler_debug.setFormatter(admin_api_formatter_debug)
admins_api_logger.addHandler(admins_api_file_handler)
admins_api_logger.addHandler(admins_api_file_handler_debug)

admin_router = APIRouter(prefix="/admins", tags=["admins"])

@admin_router.post("/add/",
                   status_code=status.HTTP_201_CREATED,
                   summary="Adds a new admin to the database",
                   responses={400: {"description": "Invalid input data"},
                              500: {"description": "Internal server error"}},
                   response_model=table_models.Response_model)
def add_admin_api(admin: table_models.Admin_for_input_api):
    try:
        admins_api_logger.info(f"Запрос на доавление в 'Admins': login={admin.login}")
        add = functions.add_admin(AdminsBase(**admin.__dict__))
        admins_api_logger.info(f"Добавлен в 'Admins': login={admin.login}")

        if add == False or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Admin_api(**add.__dict__).__dict__
        )
    except HTTPException:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': login={admin.login}",
                                exc_info=True)
        raise
    except Exception as ex:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': login={admin.login}",
                                exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@admin_router.get("/get/user/{value}",
                  status_code=status.HTTP_200_OK,
                  summary="Getting admin from database",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def get_admin_api(value: int | str, attribute: str="none"):
    try:
        admins_api_logger.info(f"Запрос на получение из 'Admins': value={value}; attribute={attribute}")
        get = functions.get_admin(value, attribute)
        admins_api_logger.info(f"Получени из 'Admins': value={value}; attribute={attribute}")

        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Admin_api(**get.__dict__).__dict__
        )
    except HTTPException:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': value={value}; attribute={attribute}",
                                exc_info=True)
        raise
    except Exception as ex:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': value={value}; attribute={attribute}",
                                exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@admin_router.get("/get/{id}",
                  status_code=status.HTTP_200_OK,
                  summary="Getting admin by user id or login from the database",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def get_admin_by_id_api(id: int):
    try:
        admins_api_logger.info(f"Запрос на получение из 'Admins': id={id}")
        get = functions.get_admin_by_id(id)
        admins_api_logger.info(f"Получен из 'Admins': id={id}")
        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Admin_api(**get.__dict__).__dict__
        )
    except HTTPException:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': id={id}",
                                exc_info=True)
        raise
    except Exception as ex:
        admins_api_logger.error(f"Произошла ошибка при записи в 'Admins': id={id}",
                                exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@admin_router.put("/put/{user_id}",
                  status_code=status.HTTP_200_OK,
                  summary="Getting admin by id",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}})
def update_admin_api(user_id: int, admin: table_models.Admin_for_update_api):
    try:
        admins_api_logger.info(f"Запрос на обновление в 'Admins': user_id={user_id}")
        admins_api_logger.debug(f"Запрос на обновление в 'Admins': user_id={user_id}; {admin.__dict__}")
        update = functions.update_admin(user_id, **admin.__dict__)
        admins_api_logger.info(f"Получени из 'Admins': user_id={user_id}")
        admins_api_logger.debug(f"Получени из 'Admins': user_id={user_id}; {admin.__dict__}")

        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{update}"}
    except HTTPException:
        admins_api_logger.error(f"Произошла ошибка при обновлении в 'Admins': user_id={user_id}; {admin.__dict__}",
                                exc_info=True)
        raise
    except Exception as ex:
        admins_api_logger.error(f"Произошла ошибка при обновлении в 'Admins': user_id={user_id}; {admin.__dict__}",
                                exc_info=True)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@admin_router.delete("/del/{user_id}",
                     status_code=status.HTTP_200_OK,
                     summary="Removing an admin from the database by user id",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}})
def del_admin_api(user_id: int):
    try:
        admins_api_logger.info(f"Запрос на удаление из 'Admins': user_id={user_id}")
        delete = functions.del_admin(user_id)
        admins_api_logger.info(f"Удален из 'Admins': user_id={user_id}")
        if delete == False or delete is None:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{delete}"}
    except HTTPException:
        admins_api_logger.error(f"произошла ошибка при удалении из 'Admins': user_id={user_id}",
                                exc_info=True)
        raise
    except Exception as ex:
        admins_api_logger.error(f"произошла ошибка при удалении из 'Admins': user_id={user_id}",
                                exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )