from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Base, create_db_and_tables, environment_reader

config = environment_reader()
engine = create_engine(f"sqlite:///{config.path}", echo=True)  # echo - логирование событий
Session = sessionmaker(engine)
