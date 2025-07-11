from configurations import create_db_and_tables, engine
from functions import *

import API
import logging

from fastapi import FastAPI

# Создание логера и устанвока уровня
main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)

# Хендлеры и форматеры
main_file_handler = logging.FileHandler(filename=f"logs/{__name__}.log", encoding="UTF-8")
main_file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Присоединение хендлеров и форматеров
main_file_handler.setFormatter(main_file_formatter)
main_logger.addHandler(main_file_handler)

create_db_and_tables(engine)
main_logger.info("База и таблицы инициированны.")

app = FastAPI()
main_logger.info("Объект FastAPI создан.")

# Регистрация роутеров
app.include_router(API.user_router)
app.include_router(API.article_router)
app.include_router(API.error_router)
app.include_router(API.admin_router)
app.include_router(API.account_router)
app.include_router(API.black_list_router)
main_logger.info("Все роутеры подключенны.")