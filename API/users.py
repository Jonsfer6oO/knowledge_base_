from fastapi import APIRouter, status, HTTPException

from users import UsersBase
from . import table_models
import functions

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/add/",
                  status_code=status.HTTP_201_CREATED,
                  summary="Adds a new user to the database",
                  responses={400: {"description": "Invalid input data"},
                             500: {"description": "Internal server error"}},
                  response_model=table_models.Response_model)
def add_user_api(user: table_models.User_for_input_api):
    try:
        adding = functions.add_user(UsersBase(**user.__dict__))
        if adding == False or adding is None :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User regestration failed"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.User_api(**adding.__dict__).__dict__)
    except HTTPException:
        raise
    except Exception as ex:
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
def get_user_api(value: int | str, attribute: str="none"):
    try:
        get = functions.get_user(value=value, attribute=attribute)
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
        raise
    except Exception as ex:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@user_router.put("/put/{id}",
                 status_code=status.HTTP_200_OK,
                 summary="Updating a user in the database",
                 responses={400: {"description": "Invalid input data"},
                            500: {"description": "Internal server error"}})
def update_user_api(id: int, user: table_models.User_for_update_api):
    try:
        update = functions.update_user(id, **user.__dict__)
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
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@user_router.delete("/del/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Removes a user from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def del_user_api(id: int):
    try:
        delete = functions.del_user(id)
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
