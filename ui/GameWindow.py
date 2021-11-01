from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from ui.CellWidget import CellWidget
from ui.SaveSudokuDialog import SaveSudokuDialog


class GameWindow(QWidget):
    current_value = "0"
    is_pen = True
    sudoku = []
    error_text = ""
    do_paint = False

    def __init__(self, parent, sudoku) -> None:
        """
        :param parent: Родитель, MainWindow
        :param sudoku: Сгенирированная судоку
        """
        super().__init__(parent)
        self.sudoku = sudoku
        self.parent = parent
        uic.loadUi('ui/game.ui', self)

        self.__setup_ui()

    """Создание стартовой сетки"""

    def __setup_ui(self) -> None:
        """Отображение первоначального ui"""
        self.apply.clicked.connect(self.__do_event)
        self.__init_gui_sudoku()
        self.__init_radio_buttons()

    def __init_radio_buttons(self) -> None:
        """Отображаем radio buttons: цифры 1-9 и ручка/карандаш"""
        radios = (self.radio1, self.radio2, self.radio3, self.radio4,
                  self.radio5, self.radio6, self.radio7, self.radio8,
                  self.radio9, self.radio100)
        for radio in radios:
            radio.toggled.connect(self.__change_digit)

        self.radio_pen.toggled.connect(self.__change_brush)
        self.radio_pencil.toggled.connect(self.__change_brush)

    def __init_gui_sudoku(self) -> None:
        """Отображаем стартовое поле судоку"""
        c = 0
        for i in range(9):
            for j in range(9):
                from ui.CellWidget import CellWidget
                cell = CellWidget(self)
                cell.setObjectName(f"cell{str(i) + str(j)}")
                cell.button.setObjectName(f"btn{str(i) + str(j)}")
                if self.sudoku.start_field[i][j] != 0:
                    cell.button.setText(str(self.sudoku.start_field[i][j]))
                    cell.button.setStyleSheet('QPushButton {color: blue}')
                    cell.button.setEnabled(False)
                    c += 1
                elif self.sudoku.current_field[i][j] != 0:
                    cell.button.setText(str(self.sudoku.current_field[i][j]))
                    cell.button.setStyleSheet('QPushButton {color: black}')
                else:
                    cell.button.setText("")
                self.ui_field.addWidget(cell.button, i, j)
        print(c)

    """Слушатели"""

    def __change_digit(self) -> None:
        """Меняем выбранную цифру"""
        name = self.sender().objectName()
        print(name)
        self.current_value = name[5:]

    def __change_brush(self) -> None:
        """Меняем ручку на карандаш или наоборот"""
        name = self.sender().objectName()[6:]
        print(name)
        self.is_pen = name == "pen"

    """Применить действия"""

    def __do_event(self):
        text = str(self.event.currentText())
        print(text)
        if text == "Сохранить игру":
            self.__save_sudoku()
        elif text == "Подсказать следующий ход":
            i, j, value = self.sudoku.get_hint()
            cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
            cell.draw_pen(str(value))
            self.sudoku.current_field[i][j] = value
        elif text == "Разметить поле карандашом":
            self.__draw_pencil_all()

    def __save_sudoku(self) -> None:
        """Запускаем диалоговое окно сохранения судоку"""
        save = SaveSudokuDialog(self.parent, self.sudoku)
        save.show()

    def __draw_pencil_all(self) -> None:
        """Помечаем карандашом все клетки"""
        for i in range(9):
            for j in range(9):
                cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
                cell.draw_all_variants(j, i)

    """Перерисовка экрана"""

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Перерисовка экрана:
        Изменение текста
        Перерисовка ячеек с карандашом
        """
        self.error.setText(self.error_text)
        if self.do_paint:
            for i in range(9):
                for j in range(9):
                    cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
                    cell.update_button()

            self.do_paint = False
