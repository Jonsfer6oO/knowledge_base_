from sqlalchemy import select

from users import UsersBase, ArticlesBase
from configurations import Session

def add_user(UsersBase: object) -> bool:
    with Session() as session:
        try:
            session.add(object)
        except:
            session.rollback()  # Отменяет все незафиксированные изменения.
            return False
        else:
            session.commit()
            return True

def get_user(value: int | str, attribute: str = "none") -> UsersBase | None:
    """
        Function to get user objects.

        Parameters:
            -  atribute - may be 'id' or 'login';
            -  value - sqarch value.

        Warning:
            If **attribute** == 'none' or other, then search will be **attribute** == id.

    """

    with Session() as session:
        try:
            if attribute == "login":
                # Где выбрать и по какому полю.
                statement = select(UsersBase).where(UsersBase.login==value)
            else:
                statement = select(UsersBase).where(UsersBase.id==int(value))

            # Вернуть первый объект с типом python. all - вернет все объекты.
            db_object = session.scalar(statement).one()

            return db_object

        except:
            return False

def update_user(id: int, **new_values) -> bool:
    """
    Function for updating user objects.

    Parameters:
        -  id - user ID;
        -  new_values - key: attribute class, value: new value.

    Warning:
        If you pass non-existent attribute, they will be missed.
    """

    with Session() as session:
        try:
            user = get_user(id)
            for key, value in new_values.items():
                if hasattr(user, key):  # Проверка на существование атрибута.
                    setattr(user, key, value)  # Изменение значения атрибута.

            # Проверяет есть ли в сессии объект с таким же ключем. В случае успеха обновляет его.
            session.merge(user)

        except:
            session.rollback()
            return False

        else:
            session.commit()
            return True

def del_user(id: int) -> bool:
    with Session() as session:
        try:
            user = get_user(id)
            session.delete(user)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True