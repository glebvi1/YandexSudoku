import numpy as np
import random
import copy


class Sudoku:
    def __init__(self):
        self._field = np.array([])

    """
    Генерируем поле судоку с n заполнеными клетками
    n - сложность уровня (или возможное кол-во пустых строк)
    n = 0 - легкий
    n = 1 - средний
    n = 2 - сложный
    """
    def generate_field(self):
        self._field = np.array([[((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)])

        self.__mix(20)
        self.__delete_cells()

        return self

    # Считываем поле судоку из файла
    def read_field(self, filename: str):
        field = []
        for line in Sudoku.__reader(filename):
            field.append(list(map(int, line.split(" "))))
        self._field = np.array(field)
        return self

    # Красивый вывод судоку
    def beauty_print(self):
        for j, array in enumerate(self._field):
            for i, elem in enumerate(array):
                if elem != 0:
                    print(elem, end=" ")
                else:
                    print(".", end=" ")

                if (i + 1) % 3 == 0 and i != 8:
                    print("|", end=" ")

            print()
            if (j + 1) % 3 == 0 and j != 8:
                s1 = "-" * 6
                print(s1 + "+" + s1 + "-+" + s1 + "--")

    # Генератор, считывающий данные из файла
    @staticmethod
    def __reader(filename: str):
        for line in open(filename):
            yield line

    # Алгоритмы перемешивания судоку

    # Транспонирование судоку
    def transpose(self):
        self._field = self._field.transpose()

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
        self._field[j2], self._field[j1] = \
            copy.deepcopy(self._field[j1]), copy.deepcopy(self._field[j2])

    # Меняем квадраты местами по горизонтали
    def swap_square_to_horizontal(self):
        # Выбираем первый квадрат
        l = [0, 3, 6]
        j1 = random.choice(l)
        l.remove(j1)

        # Выбираем второй квадрат
        j2 = random.choice(l)

        # Меняем их местами
        self._field[j1: (j1 + 3)], self._field[j2: (j2 + 3)] = \
            copy.deepcopy(self._field[j2: (j2 + 3)]), copy.deepcopy(self._field[j1: (j1 + 3)])

    # Меняем квадраты местами по вертикали
    def swap_square_to_vertical(self):
        self.transpose()
        self.swap_square_to_horizontal()
        self.transpose()

    # Перемешиваем судоку, используя алгоритмы n раз
    def __mix(self, n: int):
        mix_func = ["self.transpose()",
                    "self.swap_rows()",
                    "self.swap_columns()",
                    "self.swap_square_to_horizontal()",
                    "self.swap_square_to_vertical()"]

        for i in range(n):
            func = random.choice(mix_func)
            eval(func)

    # Удаляем некоторые ячейки, после перемешивания судоку
    def __delete_cells(self):
        looks_cells = [[False for j in range(9)] for i in range(9)]
        it = 0

        while it < 81:
            # Берем рандомную ячейку
            i, j = random.randint(0, 8), random.randint(0, 8)

            # Еще не проверяли ячейку
            if not looks_cells[i][j]:
                it += 1

                temp = self._field[i][j]
                self._field[i][j] = 0

                # Возможные цифры на это поле
                option_elem = self._generate_cell_value(j, i)

                if len(option_elem) != 1:
                    self._field[i][j] = temp
                    continue
                else:
                    self._field[i][j] = 0

                looks_cells[i][j] = True

    # Метод, возращаем все возможные варианты клеток для поля (j; i) в виде кортежа
    def _generate_cell_value(self, i, j) -> tuple:
        values = []
        for v in range(1, 10):
            if self.__check_cell(i, j, v):
                values.append(v)
        return tuple(values)

    # Проверка, можно ли поставить цифру number на вертикале i+1 (нумерация с 0)
    def __check_vertical(self, i, number):
        for array in self._field:
            for ind, elem in enumerate(array):
                if ind == i and elem == number:
                    return False

        return True

    # Проверка, можно ли поставить цифру number на горизонтали j+1 (нумерация с 0)
    def __check_horizontal(self, j, number):
        return False if number in self._field[j] else True

    # Проверка, можно ли поставить цифру number в этот квадрат
    def __check_square(self, i, j, number):
        # Правый верхний угол квадрата
        start_i = 3 * (i // 3)
        start_j = 3 * (j // 3)

        # Проверяем верхнюю горизонталь и правую вертикаль
        # Для первого квадрата с координатами (0; 0): (0; 0), (0; 1), (0; 2), (1; 0), (2; 0)
        for ind in range(3):
            if number == self._field[start_j, start_i + ind] or \
                    number == self._field[start_j + ind, start_i]:
                return False

        # Координаты центра квадрата
        start_j += 1
        start_i += 1

        # Проверяем клетки квадрата 2x2
        # Для первого квадрата с координатами (0; 0): (1; 1), (1; 2), (2; 1)
        for ind in range(2):
            if number == self._field[start_j, start_i + ind] or \
                    number == self._field[start_j + ind, start_i]:
                return False

        # Проверка последней клетки
        # Для первого квадрата с координатами (0; 0): (2; 2)
        return False if number == self._field[start_j + 1, start_i + 1] else True

    # Проверка, можно ли поставить цифру number на поле (j; i)
    def __check_cell(self, i, j, number):
        return self.__check_horizontal(j, number) and \
            self.__check_vertical(i, number) and \
            self.__check_square(i, j, number)

    def get(self):
        return self._field

