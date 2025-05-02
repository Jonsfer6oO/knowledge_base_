from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

from dataclasses import dataclass
from environs import Env

def create_db_and_tables(engine) -> None:
    Base.metadata.create_all(engine)

def environment_reader():
    env = Env()
    env.read_env()

    config = Configurate(path=env("database_path"))

    return config

@dataclass
class Configurate:
    path: str

class Base(DeclarativeBase):
    pass
