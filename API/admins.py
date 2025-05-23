from fastapi import APIRouter, status, HTTPException

from admins import AdminsBase
from . import table_models
import functions

admin_router = APIRouter(prefix="/admins", tags=["admins"])

@admin_router.post("/add/",
                   status_code=status.HTTP_201_CREATED,
                   summary="Adds a new admin to the database",
                   responses={400: {"description": "Invalid input data"},
                              500: {"description": "Internal server error"}},
                   response_model=table_models.Response_model)
def add_admin_api(admin: table_models.Admin_for_input_api):
    try:
        add = functions.add_admin(AdminsBase(**admin.__dict__))
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
        raise
    except Exception as ex:
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
        get = functions.get_admin(value, attribute)
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
        raise
    except Exception as ex:
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
        get = functions.get_admin_by_id(id)
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
        raise
    except Exception as ex:
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
        update = functions.update_admin(user_id, **admin.__dict__)
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

@admin_router.delete("/del/{user_id}",
                     status_code=status.HTTP_200_OK,
                     summary="Removing an admin from the database by user id",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}})
def del_admin_api(user_id: int):
    try:
        delete = functions.del_admin(user_id)
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