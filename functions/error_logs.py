from sqlalchemy import select
from typing import List

from error_logs import ErrorsBase
from configurations import Session

def add_errors(obj: ErrorsBase) -> bool:
    with Session() as session:
        try:
            session.add(obj)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True

def get_error_by_id(id: int) -> ErrorsBase:
    with Session() as session:
        try:
            statement = select(ErrorsBase).where(ErrorsBase.id==int(id))
            db_object = session.scalars(statement).first()

            _ = db_object.user_errors

            return db_object

        except:
            return False

def get_errors_by_user_id(user_id: int) -> List[ErrorsBase]:
    with Session() as session:
        try:
            statement = select(ErrorsBase).where(ErrorsBase.id_user==int(user_id))

            db_object = session.scalars(statement).all()

            elem: ErrorsBase
            for elem in db_object:
                _ = elem.user_errors

            return db_object

        except:
            return False