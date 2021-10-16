import copy

from model.Sudoku import Sudoku


class SudokuSolver(Sudoku):
    def __init__(self, sudoku: Sudoku):
        super().__init__()
        self.sudoku = sudoku
        self.solved_sudoku = copy.deepcopy(sudoku)

    # Метод решает судоку
    def solve(self):
        # Возможные варианты цифры для соответствующего поля
        option_solved = [[(0,) for _ in range(9)] for _ in range(9)]

        # Кол-во заполненых полей в судоку
        filled_cells = 0

        for j, array in enumerate(self.solved_sudoku._field):
            for i, cell in enumerate(array):
                filled_cells += 1

                # Для пустого поля
                if cell == 0:
                    # Генерируем все возможные варинты для поля (j; i)
                    values = self.solved_sudoku._generate_cell_value(i, j)

                    # Решений нет
                    if len(values) == 0:
                        # TODO: собственное исключение
                        return None

                    # Решение единственно, сохраняем его и вызываем этот метод еще раз
                    elif len(values) == 1:
                        self.solved_sudoku._field[j, i] = values[0]
                        option_solved[j][i] = 0,

                        # Начинаем сначала
                        return self.solve()

                    # Несколько решений
                    else:
                        option_solved[j][i] = values

                        # Клетка еще не заполнена
                        filled_cells -= 1

        # Судоку решена
        if filled_cells == 81:
            return self.solved_sudoku

        # Начинаем пербор по вариантам
        for j, array in enumerate(option_solved):
            for i, cell in enumerate(array):

                # Поле уже заполнено
                if self.solved_sudoku._field[j, i] != 0:
                    continue

                # Копируем судоку, если решение окажется неверным
                #copy_sudoku = copy.deepcopy(self.solved_sudoku._field)
                #copy_options_solved = copy.deepcopy(option_solved)

                for index in range(len(cell)):
                    number = cell[index]
                    self.solved_sudoku._field[j, i] = number

                    solver = self.solve()

                    # Возращаемся на шаг назад
                    if solver is None:
                        #self.solved_sudoku._field = copy.deepcopy(copy_sudoku)
                        #option_solved = copy.deepcopy(copy_options_solved)
                        self.solved_sudoku._field[j, i] = 0
                        return self.solved_sudoku
                    else:
                        return solver

        return self

