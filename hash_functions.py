import hashlib
import os

def hashed_password(password: str) -> tuple:
    new_password = password.encode()
    salt: bytes = os.urandom(16)

    dk = hashlib.pbkdf2_hmac(hash_name="sha256",
                        password=new_password,
                        salt=salt,
                        iterations=100000)

    return salt, dk.hex()
