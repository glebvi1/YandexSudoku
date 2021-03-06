import sqlite3
from typing import Optional

from dao.db_users_handler import update_user
from model import Sudoku
from model.User import User


def save_sudoku(sudoku: Sudoku, user: User) -> User:
    """Сохранение судоку в БД
    :param sudoku: судоку, которую сохраняем
    :param user: пользователь, котороый сохраняет судоку
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO sudokus (filename, time, count_hint, is_solved, n, uid)"
                   f"VALUES {sudoku.filename, sudoku.time, sudoku.count_hints, sudoku.is_solved, sudoku.n, user.uid}")
    connection.commit()

    sid = cursor.lastrowid
    sudoku.sid = sid
    user.sudokus.append(sid)

    cursor.close()
    connection.close()

    update_user(user)
    return user


def find_sudoku_by_filename(filename: str, user: User, sudoku: Sudoku) -> Sudoku:
    """Ищем судоку в БД по имени файла и пользователю
    :param filename: имя файл
    :param user: пользователь
    :param sudoku: судоку, в которую записываем данные
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    sudoku_db = cursor.execute(f"SELECT * FROM sudokus as s "
                   f"WHERE s.filename='{filename}' AND s.uid={user.uid}").fetchall()

    sudoku.sid = sudoku_db[0][0]
    sudoku.filename = sudoku_db[0][1]
    sudoku.time = sudoku_db[0][2]
    sudoku.count_hints = sudoku_db[0][3]
    sudoku.is_solved = bool(sudoku_db[0][4])
    sudoku.n = sudoku_db[0][5]
    sudoku.uid = sudoku_db[0][6]

    cursor.close()
    connection.close()

    return sudoku


def update_sudoku(sudoku: Sudoku, user: User) -> None:
    """ Обновляем данные судоку
    :param sudoku: новая судоку
    :param user: пользователь
    """
    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()

    cursor.execute(f"UPDATE sudokus SET time='{sudoku.time}', count_hint={sudoku.count_hints}, "
                   f"is_solved={sudoku.is_solved}"
                   f" WHERE filename='{sudoku.filename}' AND uid={user.uid}")
    connection.commit()

    cursor.close()
    connection.close()


def get_sudokus_by_sids(sids: list) -> Optional[list]:
    """Получаем судоку по id
    :param sids: лист id-ников
    """
    if sids is None:
        return None

    connection = sqlite3.connect("dao/sudoku.db")
    cursor = connection.cursor()
    sudokus = []

    for sid in sids:
        sudoku = cursor.execute(f"SELECT * FROM sudokus WHERE sid={sid}").fetchone()
        sudokus.append(sudoku)

    cursor.close()
    connection.close()

    return sudokus
