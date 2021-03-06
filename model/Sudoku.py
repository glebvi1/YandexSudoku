from __future__ import annotations

import base64
import copy
import random
from pathlib import Path
from typing import Tuple, Optional
from typing import Union

import numpy as np

from dao.db_sudokus_handler import save_sudoku, find_sudoku_by_filename, update_sudoku
from model.User import User


class Sudoku:

    """Конструкторы"""

    def __init__(self, n=0, is_generated=True) -> None:
        """
        :param n: сложность сгенирированной судику
        :param is_generated: нужно ли генерировать судоку
        """
        self.n = n
        self.count_hints = 0
        self.time = "00:00:00"
        self.is_solved = False
        self.filename = ""

        self.field = np.array([])

        # Текущее состояние поля
        self.current_field = np.array([])

        # Поля для решения судоку программой
        self.solved_field = np.array([])
        self.__open_cells = 0

        # Начальное поле
        self.start_field = np.array([])

        if is_generated:
            self.__generate_field()

    @classmethod
    def sudoku_from_file(cls, filename: str, user=None) -> Sudoku:
        """Создаем судоку по имени файла. Может бросать FileNotFoundError
        :param filename: имя файла, с которого генерируется судоку
        :param user: пользователь
        """
        return cls(is_generated=False).__upload_play(filename, user)

    """Генерация судоку"""

    def __generate_field(self) -> Sudoku:
        """
        Генерируем поле судоку с n заполнеными клетками
        n - сложность уровня (или возможное кол-во пустых строк)
        n = 0 - легкий
        n = 1 - средний
        n = 2 - сложный
        """
        self.field = np.array([[((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)])
        self.__mix(100)

        if self.n == 0:
            self.__delete_cells(81)
        elif self.n == 1:
            self.__delete_cells(51)  # 30 открытых клеток
        else:
            self.__delete_cells(54)  # 27 открытых клеток

        return self

    def __delete_cells(self, difficulty) -> None:
        """Удаляем клетки после перемешивания судоку
        :param difficulty: количество открытых клеток; если алгоритм легкий,
        то difficulty=81
        """
        ind = 0
        open_cells = 0
        looks_cells = [[False for _ in range(9)] for _ in range(9)]
        self.start_field = copy.deepcopy(self.field)

        while ind < 81 and open_cells != difficulty:
            i, j = random.randint(0, 8), random.randint(0, 8)

            if not looks_cells[i][j]:
                ind += 1

                temp = self.start_field[i][j]
                self.start_field[i][j] = 0
                self.solved_field = copy.deepcopy(self.start_field)

                is_solvable = self.__solve_hard_sudoku() if difficulty != 81 else self.__solve_easy_sudoku()
                if not is_solvable:
                    self.start_field[i][j] = temp
                else:
                    open_cells += 1

                looks_cells[i][j] = True

        self.current_field = copy.deepcopy(self.start_field)

    def __solve_easy_sudoku(self, one_digit=False) -> Union[bool, tuple]:
        """Решаем судоку простым способом
        :param one_digit: угадать первое число
        """
        open_cells = 0
        for i, arr in enumerate(self.solved_field):
            for j, elem in enumerate(arr):
                if elem != 0:
                    open_cells += 1
                    continue
                values = self.generate_cell_value(j, i, is_solved_field=True)
                if len(values) == 1:

                    if one_digit:
                        self.__open_cells = 0
                        return i, j, values[0]
                    self.solved_field[i][j] = values[0]
                    open_cells += 1
                    continue
                elif len(values) == 0:
                    return False

        if one_digit:
            return False
        if open_cells == 81:
            self.__open_cells = 0
            return True
        if self.__open_cells == open_cells:
            self.__open_cells = 0
            return False
        else:
            self.__open_cells = open_cells
            self.__solve_easy_sudoku()

    def __solve_hard_sudoku(self) -> bool:
        """Метод решает судоку перебором всех возможных вариантов"""
        solve = self.__solve_easy_sudoku()
        if solve:
            return True

        for i, arr in enumerate(self.solved_field):
            for j, elem in enumerate(arr):
                if elem != 0:
                    continue
                for possible_variation in self.generate_cell_value(j, i, is_solved_field=True):
                    self.solved_field[i][j] = possible_variation

                    if self.__solve_hard_sudoku():
                        return True
                    else:
                        self.solved_field[i][j] = 0
                return False
        return True

    """Работа с текущим полем"""

    def is_correct_event(self, i, j, value: int) -> bool:
        """ Проверяем, возможно ли self.current_field[i][j] = value
        :param i: номер столбца
        :param j: номер строки
        :param value: значение
        """
        return self.__check_cell(i, j, value, is_main_field=False)

    def is_win(self) -> bool:
        """Решена ли судоку?"""
        for i in range(9):
            for j in range(9):
                if self.field[i][j] != self.current_field[i][j]:
                    return False
        self.is_solved = True
        return True

    def get_hint(self) -> Tuple[int, int, int]:
        """Метод подсказывает следующий ход"""
        self.solved_field = copy.deepcopy(self.current_field)
        results = self.__solve_easy_sudoku(one_digit=True)

        if isinstance(results, bool):
            min_variants = 9
            min_i = 0
            min_j = 0
            for i in range(9):
                for j in range(9):
                    if self.current_field[i][j] != 0:
                        continue
                    values = self.generate_cell_value(j, i, is_main_field=False)
                    l = len(values)
                    if l < min_variants:
                        min_variants = l
                        min_i = i
                        min_j = j
            return min_i, min_j, self.field[min_i][min_j]

        return results

    """Алгоритмы перемешивания судоку"""

    def transpose(self) -> None:
        """Транспонирование судоку"""
        self.field = self.field.transpose()

    def swap_rows(self) -> None:
        """Меняем строки местами в пределах одного квадрата"""
        self.transpose()
        self.swap_columns()
        self.transpose()

    def swap_columns(self) -> None:
        """Меняем столбцы местами пределах одного квадрата"""
        # Выбираем первую колонку
        j1 = random.randint(0, 8)

        # Выбираем вторую колонку
        if j1 % 3 == 0:
            j2 = random.choice([1, 2])
        elif j1 % 3 == 1:
            j2 = random.choice([-1, 1])
        else:
            j2 = random.choice([-1, -2])
        j2 += j1

        # Меняем их местами
        self.field[j2], self.field[j1] = \
            copy.deepcopy(self.field[j1]), copy.deepcopy(self.field[j2])

    def swap_square_to_horizontal(self) -> None:
        """Меняем квадраты местами по горизонтали"""
        # Выбираем первый квадрат
        l = [0, 3, 6]
        j1 = random.choice(l)
        l.remove(j1)

        # Выбираем второй квадрат
        j2 = random.choice(l)

        # Меняем их местами
        self.field[j1: (j1 + 3)], self.field[j2: (j2 + 3)] = \
            copy.deepcopy(self.field[j2: (j2 + 3)]), copy.deepcopy(self.field[j1: (j1 + 3)])

    def swap_square_to_vertical(self) -> None:
        """Меняем квадраты местами по вертикали"""
        self.transpose()
        self.swap_square_to_horizontal()
        self.transpose()

    def __mix(self, n: int) -> None:
        """Перемешиваем судоку
        :param n: количество перемешиваний
        """
        mix_func = (self.transpose,
                    self.swap_rows,
                    self.swap_columns,
                    self.swap_square_to_horizontal,
                    self.swap_square_to_vertical)

        for i in range(n):
            func = random.choice(mix_func)
            func()

    def generate_cell_value(self, i: int, j: int, is_solved_field=False,
                            is_main_field=True) -> tuple:
        """Возращаем все возможные варианты клеток для поля (j; i) в виде кортежа
        :param i: номер столбца
        :param j: номер строки
        :param is_solved_field: использовать поле solved_field, иначе is_main_field
        :param is_main_field: использователь поле filed, иначе current_field
        """
        values = []
        for v in range(1, 10):
            if self.__check_cell(i, j, v, is_solved_field, is_main_field):
                values.append(v)
        return tuple(values)

    """Проверки на цифры"""

    def __check_vertical(self, i: int, number: int, is_solved_field=False,
                         is_main_field=True) -> bool:
        """ Проверка, можно ли поставить цифру number на вертикале i+1 (нумерация с 0)
        :param i: номер вертикали
        :param number: значение, которое проверяем
        :param is_solved_field: использовать поле solved_field, иначе is_main_field
        :param is_main_field: использователь поле filed, иначе current_field
        """
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable
        for array in iterable:
            for ind, elem in enumerate(array):
                if ind == i and elem == number:
                    return False

        return True

    def __check_horizontal(self, j: int, number: int, is_solved_field=False,
                           is_main_field=True) -> bool:
        """Проверка, можно ли поставить цифру number на горизонтали j+1 (нумерация с 0)
        :param j: номер строки
        :param number: значение, которое проверяем
        :param is_solved_field: использовать поле solved_field, иначе is_main_field
        :param is_main_field: использователь поле filed, иначе current_field
        """
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable
        return False if number in iterable[j] else True

    def __check_square(self, i: int, j: int, number, is_solved_field=False,
                       is_main_field=True) -> bool:
        """Проверка, можно ли поставить цифру number в этот квадрат
        :param i: номер строки
        :param j: номер столбца
        :param number: значение, которое проверяем
        :param is_solved_field: использовать поле solved_field, иначе is_main_field
        :param is_main_field: использователь поле filed, иначе current_field
        """
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable

        start_i = i - i % 3
        start_j = j - j % 3
        for ii in range(start_i, start_i + 3):
            for jj in range(start_j, start_j + 3):
                if iterable[jj][ii] == number:
                    return False
        return True

    def __check_cell(self, i: int, j: int, number: int, is_solved_field=False,
                     is_main_field=True) -> bool:
        """ Проверка, можно ли поставить цифру number на поле (j; i)
        :param i: номер столбца
        :param j: номер строки
        :param number: значение, которое проверяем
        :param is_solved_field: использовать поле solved_field, иначе is_main_field
        :param is_main_field: использователь поле filed, иначе current_field
        """
        return self.__check_horizontal(j, number, is_solved_field, is_main_field) and \
               self.__check_vertical(i, number, is_solved_field, is_main_field) and \
               self.__check_square(i, j, number, is_solved_field, is_main_field)

    """Сохранение/загрузка/обновление игры"""

    @staticmethod
    def __create_directory(user: User) -> str:
        """Создаем папки для хранения полей судоку в файлах
        :param user: пользователь
        """
        Path("files").mkdir(parents=True, exist_ok=True)

        path = f"saved_sudoku_{user.uid}/" if user is not None else "local_sudoku/"
        path = "files/" + path
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def update_sudoku(self, time: str, count_hints: int, is_solved: bool, user: User) -> None:
        """ Обновляем судоку
        :param time: новое время
        :param count_hints: новое кол-во подсказок
        :param is_solved: решена/не решена
        :param user: пользователь
        """
        self.count_hints = count_hints
        self.time = time
        self.is_solved = is_solved

        self.save_game(self.filename[:-4], time, count_hints, user, is_saving_in_db=False)
        update_sudoku(self, user)

    def save_game(self, name: str, time: str, count_hints: int, user=None, is_saving_in_db=True) -> Optional[User]:
        """ Сохраняем судоку в файл
        :param name: имя файла без расширения
        :param time: время
        :param count_hints: кол-во подсказок
        :param user: пользователь
        :param is_saving_in_db: сохранять ли судоку в БД
        """

        self.count_hints = count_hints
        cur_field, field, start_field, str_count_hints = self.__encoding()
        path = Sudoku.__create_directory(user)

        with open(path + name + ".txt", "w+", encoding="utf-8") as file:
            file.write(str(cur_field) + "\n")
            file.write(str(field) + "\n")
            file.write(str(start_field) + "\n")
            if user is None:
                file.write(time + "\n")
                file.write(str(str_count_hints))
                return None

        self.filename = name + ".txt"
        self.time = time
        self.count_hints = count_hints

        if is_saving_in_db:
            return save_sudoku(self, user)

    @staticmethod
    def __upload_play(name: str, user=None) -> Sudoku:
        """ Загружаем игру из файла
        :param name: Имя файла без расширения
        :param user: пользователь
        """
        path = Sudoku.__create_directory(user)

        count_hints = None
        time = "00:00:00"

        file_data = []

        for ind, line in enumerate(Sudoku.__reader(path + name + ".txt")):
            file_data.append(line)

        encoding_cur_field = file_data[0][1:]
        encoding_field = file_data[1][1:]
        encoding_start_field = file_data[2][1:]
        if len(file_data) == 5:
            time = file_data[3]
            count_hints = file_data[4][1:]

        # Дешифруем поля, получаем строки
        current_field, field, start_field = Sudoku.__decoding(encoding_cur_field.encode("utf-8"),
                                                              encoding_field.encode("utf-8"),
                                                              encoding_start_field.encode("utf-8"))
        if count_hints is not None:
            count_hints = base64.b64decode(count_hints[1:]).decode("utf-8")
            count_hints = int(count_hints)

        sudoku = Sudoku(is_generated=False)
        sudoku.current_field = Sudoku.__str_to_sudoku(current_field)
        sudoku.field = Sudoku.__str_to_sudoku(field)
        sudoku.start_field = Sudoku.__str_to_sudoku(start_field)

        if user is not None:
            sudoku = find_sudoku_by_filename(name + ".txt", user, sudoku)
        else:
            sudoku.time = time
            sudoku.count_hints = count_hints

        return sudoku

    def __encoding(self) -> Tuple[bytes, bytes, bytes, bytes]:
        """Кодируем игровые поля и кол-во подсказок"""
        current_field_str = Sudoku.__sudoku_to_str(self.current_field)
        field_str = Sudoku.__sudoku_to_str(self.field)
        start_field_str = Sudoku.__sudoku_to_str(self.start_field)
        counts_hint = str(self.count_hints)

        return base64.b64encode(current_field_str.encode("utf-8")), \
               base64.b64encode(field_str.encode("utf-8")), \
               base64.b64encode(start_field_str.encode("utf-8")), \
               base64.b64encode(counts_hint.encode("utf-8"))

    @staticmethod
    def __decoding(current_field: bytes, field: bytes, start_field: bytes) -> Tuple[str, str, str]:
        """Декодируем поля из файла
        :param current_field: текущее поле
        :param field: заполненое поле
        :param start_field: начальное поле
        """
        return base64.b64decode(current_field).decode("utf-8"), \
               base64.b64decode(field).decode("utf-8"), \
               base64.b64decode(start_field).decode("utf-8")

    """Работа со строками/файлами"""

    def read_field(self, filename: str) -> Sudoku:
        """Считываем поле судоку из файла
        :param filename: имя файла
        """
        field = []
        for line in Sudoku.__reader(filename):
            field.append(list(map(int, line.split(" "))))
        self.field = np.array(field)
        return self

    @staticmethod
    def __reader(filename: str) -> str:
        """ Генератор, считывающий данные из файла
        :param filename: имя файла
        """
        for line in open(filename):
            yield line

    @staticmethod
    def __sudoku_to_str(sudoku: np.ndarray) -> str:
        """Переводим поле в строку
        :param sudoku: поле
        """
        result = ""
        for arr in sudoku:
            for elem in arr:
                result += str(elem)
            result += "\n"
        return result

    @staticmethod
    def __str_to_sudoku(string: str) -> np.ndarray:
        """Из строчки получаем поле
        :param string: поле в виде строки
        """
        sudoku = []
        for arr in string.split("\n"):
            temp = []
            for elem in arr:
                temp.append(int(elem))
            if len(temp) != 0:
                sudoku.append(temp)

        return np.array([np.array(xi) for xi in sudoku])

    def __str__(self) -> str:
        """Красивый вывод судоку"""
        result = ""
        for j, array in enumerate(self.field):
            for i, elem in enumerate(array):
                if elem != 0:
                    result += str(elem)
                else:
                    result += "."

                if (i + 1) % 3 == 0 and i != 8:
                    result += "|"
            result += " "
            result += "\n"
            if (j + 1) % 3 == 0 and j != 8:
                s1 = "-" * 6
                result += s1 + "+" + s1 + "-+" + s1 + "--"
        return result
