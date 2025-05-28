from fastapi import APIRouter, status, HTTPException

from accounts import AccountsBase
from . import table_models
import functions

account_router = APIRouter(prefix="/accounts", tags=["accounts"])

@account_router.post("/add/",
                     status_code=status.HTTP_201_CREATED,
                     summary="Adds account data to the database",
                     responses={400: {"description": "Invalid input data"},
                                500: {"description": "Internal server error"}},
                     response_model=table_models.Response_model)
def add_account_api(account: table_models.Account_for_input_api):
    try:
        add = functions.add_account(AccountsBase(**account.__dict__))
        if add == False or add is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type = "success",
            data = table_models.Account_api(**add.__dict__).__dict__
        )
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@account_router.get("/get/{value}",
                    status_code=status.HTTP_200_OK,
                    summary="Getting an account from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}},
                    response_model=table_models.Response_model)
def get_account_api(value: int | str, attribute="none"):
    try:
        get = functions.get_account(value, attribute)
        if get == False or get is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="Bad request"
            )

        return table_models.Response_model(
            type = "success",
            data = table_models.Account_api(**get.__dict__).__dict__
        )
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

@account_router.put("/put/{id}",
                    status_code=status.HTTP_200_OK,
                    summary="Account updates from the database",
                    responses={400: {"description": "Invalid input data"},
                               500: {"description": "Internal server error"}})
def update_account_api(id: int, account: table_models.Account_for_update_api):
    try:
        update = functions.update_account(id, **account.__dict__)
        if update == False or update is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
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

@account_router.delete("/del/{id}",
                       status_code=status.HTTP_200_OK,
                       summary="Removing an account from the database",
                       responses={400: {"description": "Invalid input data"},
                                  500: {"description": "Internal server error"}})
def del_account_api(id: int):
    try:
        delete = functions.del_account(id)
        if delete == False or delete is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
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