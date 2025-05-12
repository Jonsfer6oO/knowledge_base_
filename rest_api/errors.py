from fastapi import (
    HTTPException,
    status
)

unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="invalid username or password")