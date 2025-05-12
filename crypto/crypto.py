from pathlib import Path
import jwt
from datetime import datetime, timedelta, timezone

from configurations import config

def encode_jwt(payload: dict[str],
                private_key: str | bytes = config.JWT.private_path.read_text(),
                algorithm: str = config.JWT.alg,
                expire_timedelta: timedelta = timedelta(minutes=config.JWT.min)) -> str:

    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + expire_timedelta

    to_encode.update(
        exp = expire,
        iat = now
    )
    encode = jwt.encode(payload=payload,
                         key = private_key,
                         algorithm=algorithm)
    return encode

def decode_jwt(token: str | bytes,
               public_key: str | bytes = config.JWT.public_path,
               algorithm: str = config.JWT.alg) -> any:

    decode = jwt.decode(jwt = token,
                        key = public_key,
                        algorithms=[algorithm])
    return decode