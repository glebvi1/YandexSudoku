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
        return cls().__upload_play(filename)

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
        self.__mix(50)

        if self.n == 0:
            diff = 32
        elif self.n == 1:
            diff = 30
        else:
            diff = 27

        self.__delete_cells(diff)
        return self

    def __delete_cells(self, diff):
        """Удаляем клетки после перемешивания судоку"""
        ind = 0
        looks_cells = [[False for _ in range(9)] for _ in range(9)]
        field = copy.deepcopy(self.field)

        while ind < 81:
            i, j = random.randint(0, 8), random.randint(0, 8)

            if not looks_cells[i][j]:
                ind += 1

                temp = self.field[i][j]
                self.field[i][j] = 0

                option_elem = self._generate_cell_value(j, i)
                print(self.field)
                print(option_elem)
                if len(option_elem) != 1:
                    self.field[i][j] = temp
                    continue
                else:
                    self.field[i][j] = 0
                looks_cells[i][j] = True

        print(field, self.field, self.current_field, self.start_field, sep="\n")
        self.current_field = copy.deepcopy(self.field)
        self.start_field = copy.deepcopy(self.field)
        self.field = copy.deepcopy(field)

    def get_square_on_field(self, i, j):
        if i <= 2:
            start_i = 0
        elif i <= 5:
            start_i = 3
        else:
            start_i = 6
        if j <= 2:
            start_j = 0
        elif j <= 5:
            start_j = 3
        else:
            start_j = 6
        coords = []

        for cur_i in range(start_i, start_i + 3):
            for cur_j in range(start_j, start_j + 3):
                coords.append((cur_i, cur_j))

        return coords

    def solve(self):
        """Определяем, есть ли у судоку единственное решение"""
        # Возможные варианты цифры для соответствующего поля
        option_solved = [[(0,) for _ in range(9)] for _ in range(9)]

        # Кол-во заполненых полей в судоку
        filled_cells = 0

        for j, array in enumerate(self.solved_field):
            for i, cell in enumerate(array):
                filled_cells += 1

                # Для пустого поля
                if cell == 0:
                    # Генерируем все возможные варинты для поля (j; i)
                    values = self._generate_cell_value(i, j)

                    # Решений нет
                    if len(values) == 0:
                        # TODO: собственное исключение
                        return None

                    # Решение единственно, сохраняем его и вызываем этот метод еще раз
                    elif len(values) == 1:
                        self.solved_field[j][i] = values[0]
                        option_solved[j][i] = 0,
                        continue

                    # Несколько решений
                    else:
                        option_solved[j][i] = values

                        # Клетка еще не заполнена
                        filled_cells -= 1

        print(self.__open_cells, filled_cells)
        # Судоку решена
        if filled_cells == 81:
            self.__open_cells = 0
            return True
        elif self.__open_cells == filled_cells:
            self.__open_cells = 0
            return False
        else:
            self.__open_cells = filled_cells
            return self.solve()

    """Работа с текущим полем"""

    def is_correct_event(self, i, j, value: int):
        return self.__check_cell(i, j, value, is_main_field=False)

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
    def _generate_cell_value(self, i, j) -> tuple:
        values = []
        for v in range(1, 10):
            if self.__check_cell(i, j, v):
                values.append(v)
        return tuple(values)

    """Проверки на цифры"""

    # Проверка, можно ли поставить цифру number на вертикале i+1 (нумерация с 0)
    def __check_vertical(self, i, number, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        for array in iterable:
            for ind, elem in enumerate(array):
                if ind == i and elem == number:
                    return False

        return True

    # Проверка, можно ли поставить цифру number на горизонтали j+1 (нумерация с 0)
    def __check_horizontal(self, j, number, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        return False if number in iterable[j] else True

    # Проверка, можно ли поставить цифру number в этот квадрат
    def __check_square(self, i, j, number, is_main_field=True):
        iterable = self.field if is_main_field else self.current_field
        # Правый верхний угол квадрата
        start_i = 3 * (i // 3)
        start_j = 3 * (j // 3)

        # Проверяем верхнюю горизонталь и правую вертикаль
        # Для первого квадрата с координатами (0; 0): (0; 0), (0; 1), (0; 2), (1; 0), (2; 0)
        for ind in range(3):
            if number == iterable[start_j, start_i + ind] or \
                    number == iterable[start_j + ind, start_i]:
                return False

        # Координаты центра квадрата
        start_j += 1
        start_i += 1

        # Проверяем клетки квадрата 2x2
        # Для первого квадрата с координатами (0; 0): (1; 1), (1; 2), (2; 1)
        for ind in range(2):
            if number == iterable[start_j, start_i + ind] or \
                    number == iterable[start_j + ind, start_i]:
                return False

        # Проверка последней клетки
        # Для первого квадрата с координатами (0; 0): (2; 2)
        return False if number == iterable[start_j + 1, start_i + 1] else True

    # Проверка, можно ли поставить цифру number на поле (j; i)
    def __check_cell(self, i, j, number, is_main_field=True):
        return self.__check_horizontal(j, number, is_main_field) and \
               self.__check_vertical(i, number, is_main_field) and \
               self.__check_square(i, j, number, is_main_field)

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
            sudoku.append(np.array(temp))

        return np.array(sudoku)

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


"""while it < 81:
            i, j = random.randrange(0, 9, 1), random.randrange(0, 9, 1)
            if not was_look[i][j]:
                it += 1
                was_look[i][j] = True

                temp = self.field[i, j]
                self.field[i, j] = 0
                difficult -= 1  # Усложняем если убрали элемент

                table_solution = []
                for copy_i in range(0, 9):
                    table_solution.append(self.field[copy_i][:])  # Скопируем в отдельный список

                i_solution = 0
                for solution in solver.solve_sudoku((example.n, example.n), table_solution):
                    i_solution += 1  # Считаем количество решений

                if i_solution != 1:  # Если решение не одинственное вернуть всё обратно
                    example.table[i][j] = temp
                    difficult += 1  # Облегчаем
"""

"""
            coords = self.get_square_on_field(i, j)
            for y, array in enumerate(self.field):
                if b:
                    break
                for x, elem in enumerate(array):
                    if y == j or i == x or (x, y) in coords:
                        option_elem = self._generate_cell_value(y, x)

                        if len(option_elem) != 1:
                            continue
                        elif len(option_elem) == 1:
                            self.field[i][j] = 0
                            difficult -= 1
                            b = True
                            break
            if not b:
                self.field[i][j] = temp
"""

"""        while diff != difficult:
            inn+=1
            # Берем рандомную ячейку
            if difficult >= 55:
                i, j = random.randint(0, 8), random.randint(0, 8)
            else:
                i, j = global_i, global_j
                global_j += 1
                if global_j == 9:
                    global_j = 0
                    global_i += 1
                if global_i == 9:
                    break
            if self.field[i][j] == 0:
                continue
            #print(self.field)

            temp = self.field[i][j]
            self.field[i][j] = 0
            b = False

            self.solved_field = copy.deepcopy(self.field)

            is_solved = self.solve()
            if not is_solved or is_solved is None:
                self.field[i, j] = temp
                continue
            difficult -= 1
            print(difficult)
            if difficult % 5 == 0:
                print(self.field)
                print()
"""
