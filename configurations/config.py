from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from pydantic import BaseModel
from pathlib import Path

from dataclasses import dataclass
from environs import Env

@dataclass
class JWT_info:
    private_path: Path
    public_path: Path
    alg: str
    min: int

def create_db_and_tables(engine) -> None:
    Base.metadata.create_all(engine)

def environment_reader():
    env = Env()
    env.read_env()

    config = Configurate(path=env("database_path"),
                         JWT=JWT_info(
                             private_path=Path(env("private_path")),
                             public_path=Path(env("public_path")),
                             alg=env("ALGORITHM"),
                             min=int(env("ACCESS_TOKEN_EXPIRE_MINUTES"))
                         ))

    return config

@dataclass
class Configurate:
    path: str
    JWT: JWT_info

class Base(DeclarativeBase):
    pass
