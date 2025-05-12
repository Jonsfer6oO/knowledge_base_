from fastapi import APIRouter, Depends

from functions import get_user, add_account
from accounts import AccountsBase
from .functions import valid_auth_user
from crypto import encode_jwt
from users import UsersBase

router_users = APIRouter(prefix="/users", tags=["users"])

@router_users.get("/get/{value}/")
def get_user_API(value: int | str, attribute: str = "none"):
    return vars(get_user(value, attribute))

@router_users.post("/login/")
def auth_user_issue_jwt(user: UsersBase = Depends(valid_auth_user)):

    if user == None:
        return {
            "status": "Not found"
        }
    jwt_paylod = {
        "sub": user.login,
        "email": user.email,
        "phone": user.phone,
    }
    token = encode_jwt(payload=jwt_paylod)
    return {
        "access_token": token,
        "token_type": "Bearer"
    }

@router_users.post("/add/")
def add_account_api(login: str, password: str):
    add_account(AccountsBase(
        login = login,
        password = password
    ))
    return {
        "status": "Great!"
    }
