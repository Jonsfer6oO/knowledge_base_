from fastapi import APIRouter, status, HTTPException

from handler_logging import LokiLogginHandler
from error_logs import ErrorsBase
from . import table_models
import functions
from . import other_functions

import logging

error_api_logger = logging.getLogger(__name__)
error_api_logger.level = logging.DEBUG

error_api_file_handler = logging.FileHandler(f"logs/API/{__name__}.log", encoding="UTF-8")
error_api_file_handler_debug = logging.FileHandler(f"logs/API/{__name__}_debug.log", encoding="UTF-8")
error_api_file_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
error_api_file_loki_handler.level = logging.DEBUG
error_api_file_handler.level = logging.INFO
error_api_file_handler_debug.level = logging.DEBUG

error_api_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
error_api_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

error_api_file_handler.setFormatter(error_api_formatter)
error_api_file_handler_debug.setFormatter(error_api_formatter_debug)
error_api_file_loki_handler.setFormatter(error_api_formatter_debug)
error_api_logger.addHandler(error_api_file_handler)
error_api_logger.addHandler(error_api_file_handler_debug)
error_api_logger.addHandler(error_api_file_loki_handler)

error_router = APIRouter(prefix="/error_logs", tags=["error_logs"])

@error_router.post("/add/",
                   status_code=status.HTTP_201_CREATED,
                   summary="Adding an error record to the database",
                   responses={400: {"description": "Invalid input data"},
                              500: {"description": "Internal server error"}},
                              response_model=table_models.Response_model)
def add_error_api(error: table_models.Error_for_input_api):
    try:
        error_api_logger.info(f"Запрос на добавление в 'Errors': user_id={error.id_user}")
        add = functions.add_errors(ErrorsBase(**error.__dict__))
        error_api_logger.info(f"Добавлен в 'Errors': user_id={error.id_user}")

        if add == False  or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Error_api(**add.__dict__).__dict__)

    except HTTPException:
        error_api_logger.error(f"Произошла ошибка при добавлении в 'Errors': user_id={error.id_user}",
                               exc_info=True)
        raise
    except Exception as ex:
        error_api_logger.error(f"Произошла ошибка при добавлении в 'Errors': user_id={error.id_user}",
                               exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@error_router.get("/get/{id}/",
                  status_code=status.HTTP_200_OK,
                  summary="Getting an error from the database by id",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def get_error_by_id_api(id: int):
    try:
        error_api_logger.info(f"Запрос на получение из 'Errors': id={id}")
        get = functions.get_error_by_id(id)
        error_api_logger.info(f"Поулчен из 'Errors': id={id}")

        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Error_api(**get.__dict__).__dict__)
    except HTTPException:
        error_api_logger.error(f"Произошла ошибка при получении из 'Errors': id={id}",
                               exc_info=True)
        raise
    except Exception as ex:
        error_api_logger.error(f"Произошла ошибка при получении из 'Errors': id={id}",
                               exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@error_router.get("/get/user/{user_id}",
                  status_code=status.HTTP_200_OK,
                  summary="Getting an error from the database by user id",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def get_errors_by_user_id_api(user_id: int):
    try:
        error_api_logger.info(f"Запрос на получение из 'Errors': user_id={user_id}")
        get = functions.get_errors_by_user_id(user_id)
        error_api_logger.info(f"Поулчен из 'Errors': user_id={user_id}")

        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=other_functions.list_in_dict(get, table_models.Error_api))
    except HTTPException:
        error_api_logger.error(f"Произошла ошибкуа при получении из 'Errors': user_id={user_id}",
                               exc_info=True)
        raise
    except Exception as ex:
        error_api_logger.error(f"Произошла ошибкуа при получении из 'Errors': user_id={user_id}",
                               exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )
