import hashlib
import os

def hashed_password(password: str, salt: bytes = None) -> tuple:
    new_password = password.encode()
    if salt is None:
        salt: bytes = os.urandom(16)

    dk = hashlib.pbkdf2_hmac(hash_name="sha256",
                        password=new_password,
                        salt=salt,
                        iterations=100000)

    return salt, dk.hex()

def validate_password(secret: str, salt: bytes, password: str) -> bool:
    return secret == hashed_password(password, salt)[1]
