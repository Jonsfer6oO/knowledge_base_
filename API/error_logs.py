from fastapi import APIRouter, status, HTTPException

from error_logs import ErrorsBase
from . import table_models
import functions
from . import other_functions

error_router = APIRouter(prefix="/error_logs", tags=["error_logs"])

@error_router.post("/add/",
                   status_code=status.HTTP_201_CREATED,
                   summary="Adding an error record to the database",
                   responses={400: {"description": "Invalid input data"},
                              500: {"description": "Internal server error"}},
                              response_model=table_models.Response_model)
def add_error_api(error: table_models.Error_for_input_api):
    try:
        add = functions.add_errors(ErrorsBase(**error.__dict__))
        if add == False  or add is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Error_api(**add.__dict__).__dict__)

    except HTTPException:
        raise
    except Exception as ex:
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
        get = functions.get_error_by_id(id)
        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=table_models.Error_api(**get.__dict__).__dict__)
    except HTTPException:
        raise
    except Exception as ex:
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
        get = functions.get_errors_by_user_id(user_id)
        if get == False or get is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(type="success",
                                           data=other_functions.list_in_dict(get, table_models.Error_api))
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )
