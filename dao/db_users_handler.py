import sqlite3
from typing import Optional

from model.User import User


def login_user(login: str, password: str) -> Optional[User]:
    """Авторизация пользователя
    :param login: логин пользователя
    :param password: пароль пользователя
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    users = cursor.execute(f"SELECT * FROM users WHERE login='{login}';").fetchall()

    cursor.close()
    connection.close()

    if len(users) != 0 and users[0][3] == password:
        return User(uid=users[0][0], login=users[0][1], name=users[0][2],
                    password=users[0][3], sudokus=str_sid_to_list(users[0][4]))
    return None


def registration_user(login: str, name: str, password: str) -> Optional[User]:
    """Регистрация пользователя
    :param login: логин пользователя
    :param name: имя пользователя
    :param password: пароль пользователя
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    user_in_db = cursor.execute(f"SELECT * FROM users WHERE login='{login}';").fetchall()
    if len(user_in_db) != 0:
        return None

    cursor.execute(f"INSERT INTO users (login, name, password) VALUES {login, name, password};")
    connection.commit()

    uid = cursor.lastrowid

    cursor.close()
    connection.close()
    return User(uid=uid, login=login, name=name, password=password)


def update_user(user: User) -> None:
    """Обновляем данные пользователя
    :param user: новый пользователь
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    sid = ""
    for elem in user.sudokus:
        sid += f";{elem}"
    sid = sid[1:]

    cursor.executescript(f"UPDATE users SET sid='{sid}' WHERE uid='{user.uid}';")
    connection.commit()

    cursor.close()
    connection.close()


def str_sid_to_list(sids: str) -> list:
    """Переводим строку с судоку-id в лист
    :param sids: сторка с судоку-id
    """
    return list(map(int, sids.split(";"))) if sids is not None else None
