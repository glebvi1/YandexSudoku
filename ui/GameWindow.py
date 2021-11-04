from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from ui.CellWidget import CellWidget
from ui.SaveSudokuDialog import SaveSudokuDialog


class GameWindow(QWidget):
    current_value = "0"
    is_pen = True
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
        self.event.currentIndexChanged.connect(self.__do_event)
        self.__init_gui_sudoku()
        self.__init_radio_buttons()
        self.__init_time()

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
        whites1 = [0, 1, 2]
        whites2 = [6, 7, 8]
        black = [3, 4, 5]
        for i in range(9):
            for j in range(9):
                color = ""
                from ui.CellWidget import CellWidget
                cell = CellWidget(self)
                cell.setObjectName(f"cell{str(i) + str(j)}")
                cell.button.setObjectName(f"btn{str(i) + str(j)}")
                if self.sudoku.start_field[i][j] != 0:
                    cell.button.setText(str(self.sudoku.start_field[i][j]))
                    color = "green"
                    cell.button.setEnabled(False)
                    c += 1
                elif self.sudoku.current_field[i][j] != 0:
                    cell.button.setText(str(self.sudoku.current_field[i][j]))
                    color = "black"
                else:
                    cell.button.setText("")

                cell.color = color

                if ((i in whites1 or i in whites2) and (j in whites1 or j in whites2)) or (i in black and j in black):
                    cell.button.setStyleSheet("QPushButton {background-color: grey; color: " + color + "}")
                    cell.background_color = "grey"
                else:
                    cell.button.setStyleSheet("QPushButton {background-color: white; color: " + color + "}")
                    cell.background_color = "white"

                self.ui_field.addWidget(cell.button, i, j)
        print(c)

    def __init_time(self):
        self.time = QtCore.QTime(0, 0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.__timer_event)
        self.timer.start(1000)

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

    def __do_event(self):
        """Применить действия"""
        text = str(self.event.currentText())
        print(text)
        if text == "Сохранить игру":
            self.__save_sudoku()
        elif text == "Подсказать следующий ход":
            self.sudoku.count_hints += 1
            i, j, value = self.sudoku.get_hint()
            cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
            cell.draw_pen(str(value))
            self.sudoku.current_field[i][j] = value
        elif text == "Разметить поле карандашом":
            self.sudoku.count_hints += 1
            self.__draw_pencil_all()

    def __save_sudoku(self) -> None:
        """Запускаем диалоговое окно сохранения судоку"""
        save = SaveSudokuDialog(self, self.sudoku)
        save.show()

    def __draw_pencil_all(self) -> None:
        """Помечаем карандашом все клетки"""
        for i in range(9):
            for j in range(9):
                cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
                cell.draw_all_variants(j, i)

    def __timer_event(self):
        time_display = self.time.toString('hh:mm:ss')
        self.label_timer.setText(time_display)
        self.time = self.time.addSecs(1)

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
