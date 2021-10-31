import base64
import copy
import random

import numpy as np


class Sudoku:
    def __init__(self, n=0, is_generated=True):
        self.n = n
        self.field = np.array([])

        # Текущее состояние поля
        self.current_field = []

        # Поля для решения судоку программой
        self.solved_field = []
        self.__open_cells = 0

        # Начальное поле
        self.start_field = []

        if is_generated:
            self.generate_field()

    @classmethod
    def sudoku_from_file(cls, filename: str):
        """Создаем судоку по имени файла. Может бросать FileNotFoundError"""
        return cls(is_generated=False).__upload_play(filename)

    """Генерация судоку"""

    def generate_field(self):
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

    def __delete_cells(self, difficulty):
        """Удаляем клетки после перемешивания судоку"""
        ind = 0
        open_cells = 0
        looks_cells = [[False for _ in range(9)] for _ in range(9)]
        self.start_field = copy.deepcopy(self.field)
        print(self.start_field, type(self.start_field), self.start_field.shape)

        while ind < 81 and open_cells != difficulty:
            i, j = random.randint(0, 8), random.randint(0, 8)

            if not looks_cells[i][j]:
                ind += 1

                temp = self.start_field[i][j]
                self.start_field[i][j] = 0
                self.solved_field = copy.deepcopy(self.start_field)

                is_solvable = self.solve_hard_sudoku() if difficulty != 81 else self.solve_easy_sudoku()
                if not is_solvable:
                    self.start_field[i][j] = temp
                else:
                    open_cells += 1

                looks_cells[i][j] = True

        self.current_field = copy.deepcopy(self.start_field)

    def solve_easy_sudoku(self):
        """Решаем судоку простым способом"""
        open_cells = 0
        for i, arr in enumerate(self.solved_field):
            for j, elem in enumerate(arr):
                if elem != 0:
                    open_cells += 1
                    continue
                values = self.generate_cell_value(j, i, is_solved_field=True)
                if len(values) == 1:
                    self.solved_field[i][j] = values[0]
                    open_cells += 1
                    continue
                elif len(values) == 0:
                    return False

        if open_cells == 81:
            self.__open_cells = 0
            return True
        if self.__open_cells == open_cells:
            self.__open_cells = 0
            return False
        else:
            self.__open_cells = open_cells
            self.solve_easy_sudoku()

    def solve_hard_sudoku(self):
        for i, arr in enumerate(self.solved_field):
            for j, elem in enumerate(arr):
                if elem != 0:
                    continue
                for possible_variation in self.generate_cell_value(j, i, is_solved_field=True):
                    self.solved_field[i][j] = possible_variation

                    if self.solve_hard_sudoku():
                        return True
                    else:
                        self.solved_field[i][j] = 0
                return False
        return True

    """Работа с текущим полем"""

    def is_correct_event(self, i, j, value: int):
        return self.__check_cell(i, j, value, is_main_field=False)

    def is_win(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j] != self.current_field[i][j]:
                    return False
        return True

    """Алгоритмы перемешивания судоку"""

    # Транспонирование судоку
    def transpose(self):
        self.field = self.field.transpose()

    # Меняем строки местами в пределах одного квадрата
    def swap_rows(self):
        self.transpose()
        self.swap_columns()
        self.transpose()

    # Меняем столбцы местами пределах одного квадрата
    def swap_columns(self):
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

    # Меняем квадраты местами по горизонтали
    def swap_square_to_horizontal(self):
        # Выбираем первый квадрат
        l = [0, 3, 6]
        j1 = random.choice(l)
        l.remove(j1)

        # Выбираем второй квадрат
        j2 = random.choice(l)

        # Меняем их местами
        self.field[j1: (j1 + 3)], self.field[j2: (j2 + 3)] = \
            copy.deepcopy(self.field[j2: (j2 + 3)]), copy.deepcopy(self.field[j1: (j1 + 3)])

    # Меняем квадраты местами по вертикали
    def swap_square_to_vertical(self):
        self.transpose()
        self.swap_square_to_horizontal()
        self.transpose()

    # Перемешиваем судоку, используя алгоритмы n раз
    def __mix(self, n: int):
        mix_func = (self.transpose,
                    self.swap_rows,
                    self.swap_columns,
                    self.swap_square_to_horizontal,
                    self.swap_square_to_vertical)

        for i in range(n):
            func = random.choice(mix_func)
            func()

    # Метод, возращаем все возможные варианты клеток для поля (j; i) в виде кортежа
    def generate_cell_value(self, i, j, is_solved_field=False, is_main_field=True) -> tuple:
        values = []
        for v in range(1, 10):
            if self.__check_cell(i, j, v, is_solved_field, is_main_field):
                values.append(v)
        return tuple(values)

    """Проверки на цифры"""

    # Проверка, можно ли поставить цифру number на вертикале i+1 (нумерация с 0)
    def __check_vertical(self, i, number, is_solved_field=False, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable
        for array in iterable:
            for ind, elem in enumerate(array):
                if ind == i and elem == number:
                    return False

        return True

    # Проверка, можно ли поставить цифру number на горизонтали j+1 (нумерация с 0)
    def __check_horizontal(self, j, number, is_solved_field=False, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable
        return False if number in iterable[j] else True

    # Проверка, можно ли поставить цифру number в этот квадрат
    def __check_square(self, i, j, number, is_solved_field=False, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        iterable = self.solved_field if is_solved_field else iterable
        # Правый верхний угол квадрата
        start_i = 3 * (i // 3)
        start_j = 3 * (j // 3)

        # Проверяем верхнюю горизонталь и правую вертикаль
        # Для первого квадрата с координатами (0; 0): (0; 0), (0; 1), (0; 2), (1; 0), (2; 0)
        for ind in range(3):
            if number == iterable[start_j][start_i + ind] or \
                    number == iterable[start_j + ind][start_i]:
                return False

        # Координаты центра квадрата
        start_j += 1
        start_i += 1

        # Проверяем клетки квадрата 2x2
        # Для первого квадрата с координатами (0; 0): (1; 1), (1; 2), (2; 1)
        for ind in range(2):
            if number == iterable[start_j][start_i + ind] or \
                    number == iterable[start_j + ind][start_i]:
                return False

        # Проверка последней клетки
        # Для первого квадрата с координатами (0; 0): (2; 2)
        return False if number == iterable[start_j + 1][start_i + 1] else True

    # Проверка, можно ли поставить цифру number на поле (j; i)
    def __check_cell(self, i, j, number, is_solved_field=False, is_main_field=True):
        return self.__check_horizontal(j, number, is_solved_field, is_main_field) and \
               self.__check_vertical(i, number, is_solved_field, is_main_field) and \
               self.__check_square(i, j, number, is_solved_field, is_main_field)

    """Сохранение/загрузка игры"""

    def save_game(self, name):
        cur_field, field, start_field = self.__encoding()
        with open(name + ".txt", "w+", encoding="utf-8") as file:
            file.write(str(cur_field) + "\n")
            file.write(str(field) + "\n")
            file.write(str(start_field) + "\n")

    # Загружаем игру из файла
    @staticmethod
    def __upload_play(name):
        encoding_cur_field = ""
        encoding_field = ""
        encoding_start_field = ""
        # Построчно заполняем self
        for ind, line in enumerate(Sudoku.__reader(name + ".txt")):
            if ind == 0:
                encoding_cur_field = line[1:]
            elif ind == 1:
                encoding_field = line[1:]
            elif ind == 2:
                encoding_start_field = line[1:]

        # Дешифруем поля, получаем строки
        current_field, field, start_field = Sudoku.__decoding(encoding_cur_field.encode("utf-8"),
                                                              encoding_field.encode("utf-8"),
                                                              encoding_start_field.encode("utf-8"))

        # Перевод поля из строки в поле (np.array)
        sudoku = Sudoku(is_generated=False)
        sudoku.current_field = Sudoku.__str_to_sudoku(current_field)
        sudoku.field = Sudoku.__str_to_sudoku(field)
        sudoku.start_field = Sudoku.__str_to_sudoku(start_field)
        print(sudoku.current_field, sudoku.field, sep="\n")
        return sudoku

    # Кодируем игровые поля
    def __encoding(self):
        # Переводим поля в строки
        current_field_str = Sudoku.__sudoku_to_str(self.current_field)
        field_str = Sudoku.__sudoku_to_str(self.field)
        start_field_str = Sudoku.__sudoku_to_str(self.start_field)

        # Кодируем поля
        # Возращаем байты
        return base64.b64encode(current_field_str.encode("utf-8")), \
               base64.b64encode(field_str.encode("utf-8")), \
               base64.b64encode(start_field_str.encode("utf-8"))

    # Декодируем поля из файла
    @staticmethod
    def __decoding(current_field, field, start_field):
        # Возращаем стороки
        return base64.b64decode(current_field).decode("utf-8"), \
               base64.b64decode(field).decode("utf-8"), \
               base64.b64decode(start_field).decode("utf-8")

    """Работа со строками/файлами"""

    # Считываем поле судоку из файла
    def read_field(self, filename: str):
        field = []
        for line in Sudoku.__reader(filename):
            field.append(list(map(int, line.split(" "))))
        self.field = np.array(field)
        return self

    # Генератор, считывающий данные из файла
    @staticmethod
    def __reader(filename: str):
        for line in open(filename):
            yield line

    @staticmethod
    def __sudoku_to_str(sudoku):
        result = ""
        for arr in sudoku:
            for elem in arr:
                result += str(elem)
            result += "\n"
        return result

    @staticmethod
    def __str_to_sudoku(string: str):
        sudoku = []
        for arr in string.split("\n"):
            temp = []
            for elem in arr:
                print(elem)
                temp.append(int(elem))
            sudoku.append(temp)

        return np.array([np.array(xi) for xi in sudoku])

    # Красивый вывод судоку
    def __str__(self):
        result = ""
        for j, array in enumerate(self.field):
            for i, elem in enumerate(array):
                if elem != 0:
                    result += elem
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
