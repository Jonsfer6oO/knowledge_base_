from fastapi import APIRouter, HTTPException, status

from users import ArticlesBase
from . import table_models
from . import other_functions
import functions

article_router = APIRouter(prefix="/articles", tags=["articles"])

@article_router.post("/add/",
                    status_code=status.HTTP_201_CREATED,
                    summary="Adds an article object to the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def add_article_api(article: table_models.Article_for_input_api):
    try:
        add = functions.add_article(ArticlesBase(**article.__dict__))
        if add == False or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Article_api(**article.__dict__).__dict__)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@article_router.get("get/{user_id}",
                    status_code=status.HTTP_200_OK,
                    summary="Getting article by user id",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def get_articles_by_user_id_api(user_id: int):
    try:
        get = functions.get_articles_by_user_id(user_id)
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
        raise
    except Exception as ex:
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
        get = functions.get_article_by_id(id)
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
        raise
    except Exception as ex:
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
        update = functions.update_article(id, **article.__dict__)
        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type":"success", "status": f"{update}"}

    except HTTPException:
        raise
    except Exception as ex:
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
        delete = functions.del_article(id)
        if delete == False or delete is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type":"success", "status": f"{delete}"}

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )