from fastapi import APIRouter, status, HTTPException

from black_list import BlackListBase
from . import table_models
import functions

black_list_router = APIRouter(prefix="/black_list", tags=["black_list"])

@black_list_router.post("/add/",
                     status_code=status.HTTP_201_CREATED,
                     summary="Adding user to blacklist",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}},
                     response_model=table_models.Response_model)
def add_black_list_api(black: table_models.Black_list_for_input_api):
    try:
        add = functions.add_black_list(BlackListBase(**black.__dict__))
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
        raise
    except Exception as ex:
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
        get = functions.get_user_black_list_id(id)
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
        raise
    except Exception as ex:
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
        get = functions.get_user_black_list_user_id(user_id)
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
        raise
    except Exception as ex:
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
        update = functions.update_user_black_list(user_id, **black.__dict__)
        if update == False or update is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{update}"}

    except HTTPException:
        raise
    except Exception as ex:
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
        delete = functions.del_user_black_list(user_id)
        if delete == False or delete is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return {"type": "success", "status": f"{delete}"}

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )