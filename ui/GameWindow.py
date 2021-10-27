from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from ui.SaveSudokuDialog import SaveSudokuDialog


class GameWindow(QWidget):
    current_value = "0"
    is_pen = True
    sudoku = []
    error_text = ""
    do_paint = False

    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.sudoku = sudoku
        self.parent = parent
        uic.loadUi('ui/game.ui', self)

        self.__setup_ui()

    def __setup_ui(self):
        self.btn_save.clicked.connect(self.__save_sudoku)
        self.__init_gui_sudoku()
        self.__init_radio_buttons()

    """Создание стартовой сетки"""

    def __init_radio_buttons(self):
        radios = (self.radio1, self.radio2, self.radio3, self.radio4,
                  self.radio5, self.radio6, self.radio7, self.radio8,
                  self.radio9, self.radio100)
        for radio in radios:
            radio.toggled.connect(self.__change_digit)

        self.radio_pen.toggled.connect(self.__change_brush)
        self.radio_pencil.toggled.connect(self.__change_brush)

    def __init_gui_sudoku(self):
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
                elif self.sudoku.current_field[i][j] != 0:
                    cell.button.setText(str(self.sudoku.current_field[i][j]))
                    cell.button.setStyleSheet('QPushButton {color: black}')
                else:
                    cell.button.setText("")
                self.ui_field.addWidget(cell.button, i, j)

    """Слушатели"""

    def __change_digit(self):
        name = self.sender().objectName()
        print(name)
        self.current_value = name[5:]

    def __change_brush(self):
        name = self.sender().objectName()[6:]
        print(name)
        self.is_pen = name == "pen"

    def __save_sudoku(self):
        save = SaveSudokuDialog(self.parent, self.sudoku)
        save.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.error.setText(self.error_text)
        if self.do_paint:
            from ui.CellWidget import CellWidget
            for i in range(9):
                for j in range(9):
                    cell = self.findChild(CellWidget, f"cell{str(i) + str(j)}")
                    cell.update_button()

            self.do_paint = False
