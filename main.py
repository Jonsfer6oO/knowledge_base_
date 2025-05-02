from configurations import Session, config, create_db_and_tables, engine

from admins import AdminsBase
from accounts import AccountsBase
from black_list import BlackListBase
from error_logs import ErrorsBase
from users import UsersBase, ArticlesBase

create_db_and_tables(engine)