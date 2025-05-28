from configurations import Session, config, create_db_and_tables, engine
from functions import *

import API

from fastapi import FastAPI

create_db_and_tables(engine)

app = FastAPI()

# Регистрация роутеров
app.include_router(API.user_router)
app.include_router(API.article_router)
app.include_router(API.error_router)
app.include_router(API.admin_router)
app.include_router(API.account_router)
app.include_router(API.black_list_router)