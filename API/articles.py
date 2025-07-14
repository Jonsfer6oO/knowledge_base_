from fastapi import APIRouter, HTTPException, status

from handler_logging import LokiLogginHandler
from users import ArticlesBase
from . import table_models
from . import other_functions
import functions

import logging

articles_api_logger = logging.getLogger(__name__)
articles_api_logger.level = logging.DEBUG

articles_api_file_handler = logging.FileHandler(f"logs/API/{__name__}.log", encoding="UTF-8")
articles_api_file_handler_debug = logging.FileHandler(f"logs/API/{__name__}_debug.log", encoding="UTF-8")
articles_api_file_loki_handler = LokiLogginHandler(url="http://localhost:3100/loki/api/v1/push")
articles_api_file_loki_handler.level = logging.DEBUG
articles_api_file_handler.level = logging.INFO
articles_api_file_handler_debug.level = logging.DEBUG

articles_api_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
articles_api_formatter_debug = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s")

articles_api_file_handler.setFormatter(articles_api_formatter)
articles_api_file_handler_debug.setFormatter(articles_api_formatter_debug)
articles_api_file_loki_handler.setFormatter(articles_api_formatter_debug)
articles_api_logger.addHandler(articles_api_file_handler)
articles_api_logger.addHandler(articles_api_file_handler_debug)
articles_api_logger.addHandler(articles_api_file_loki_handler)

article_router = APIRouter(prefix="/articles", tags=["articles"])

@article_router.post("/add/",
                    status_code=status.HTTP_201_CREATED,
                    summary="Adds an article object to the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def add_article_api(article: table_models.Article_for_input_api):
    try:
        articles_api_logger.info(f"Запрос на добавление в 'Articles': user_id={article.user_id}; title={article.title}")
        add = functions.add_article(ArticlesBase(**article.__dict__))
        articles_api_logger.info(f"Добавлен в 'Articlees': user_id={article.user_id}; title={article.title}")

        if add == False or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Article_api(**add.__dict__).__dict__)
    except HTTPException:
        articles_api_logger.error(f"Произошла ошибка при доваблении в 'Articles': user_id={article.user_id}; title={article.title}",
                                  exc_info=True)
        raise
    except Exception as ex:
        articles_api_logger.error(f"Произошла ошибка при доваблении в 'Articles': user_id={article.user_id}; title={article.title}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@article_router.get("/get/user/{user_id}",
                    status_code=status.HTTP_200_OK,
                    summary="Getting article by user id",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def get_articles_by_user_id_api(user_id: int):
    try:
        articles_api_logger.info(f"Запрос на получение из 'Artciles': user_id={user_id}")
        get = functions.get_articles_by_user_id(user_id)
        articles_api_logger.info(f"Получен из 'Articles': user_id={user_id}")

        if get == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=other_functions.list_in_dict(get, table_models.Article_api)
        )
    except HTTPException:
        articles_api_logger.error(f"Произошла ошибка при получении из 'Articles': user_id={user_id}",
                                  exc_info=True)
        raise
    except Exception as ex:
        articles_api_logger.error(f"Произошла ошибка при получении из 'Articles': user_id={user_id}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@article_router.get("/get/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Getting article by id",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def get_articles_by_id_api(id: int):
    try:
        articles_api_logger.info(f"Запрос на получение из 'Articles': id={id}")
        get = functions.get_article_by_id(id)
        articles_api_logger.info(f"Получен из 'Articles': id={id}")

        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type="success",
            data=table_models.Article_api(**get.__dict__).__dict__
        )
    except HTTPException:
        articles_api_logger.error(f"Произошла ошибка при получении из 'Articles': id={id}",
                                  exc_info=True)
        raise
    except Exception as ex:
        articles_api_logger.error(f"Произошла ошибка при получении из 'Articles': id={id}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@article_router.put("/put/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Update article by id",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def update_article_api(id: int,
                       article: table_models.Article_for_update_api):
    try:
        articles_api_logger.info(f"Запрос на обновление в 'Articles': id={id}")
        articles_api_logger.debug(f"Запрос на обновление в 'Articles': id={id}; {article.__dict__}")
        update = functions.update_article(id, **article.__dict__)
        articles_api_logger.info(f"Обновлен в 'Articles': id={id}")
        articles_api_logger.debug(f"Обновлен в 'Articles': id={id}; {article.__dict__}")

        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type":"success", "status": f"{update}"}

    except HTTPException:
        articles_api_logger.error(f"Произошла ошибка при обновлении в 'Articles': id={id}; {article.__dict__}",
                                  exc_info=True)
        raise
    except Exception as ex:
        articles_api_logger.error(f"Произошла ошибка при обновлении в 'Articles': id={id}; {article.__dict__}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@article_router.delete("/del/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Removes a article by id from the daabase",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def del_article_api(id: int):
    try:
        articles_api_logger.info(f"запрос на удаление из 'Articles': id={id}")
        delete = functions.del_article(id)
        articles_api_logger.info(f"Удален из 'Articles': id={id}")

        if delete == False or delete is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type":"success", "status": f"{delete}"}

    except HTTPException:
        articles_api_logger.error(f"Произошла ошибка при удалении из 'Articles': id={id}",
                                  exc_info=True)
        raise
    except Exception as ex:
        articles_api_logger.error(f"Произошла ошибка при удалении из 'Articles': id={id}",
                                  exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )