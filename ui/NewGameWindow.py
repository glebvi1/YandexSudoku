from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from GameWindow import GameWindow
from model.Sudoku import Sudoku


class NewGameWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/new_game.ui', self)
        self.buttons = (self.btn_easy, self.btn_middle, self.btn_hard)
        self.widgets = [self.label, self.label_2]
        self.widgets.extend(self.buttons)

        self.__setup_ui()

    def __setup_ui(self):
        for button in self.buttons:
            button.clicked.connect(self.__generate_sudoku)

    def __generate_sudoku(self):
        name = self.sender().objectName()[4:]

        if name == "easy":
            n = 0
        elif name == "middle":
            n = 1
        else:
            n = 2
        print(n)
        sudoku = Sudoku(n)

        for widget in self.widgets:
            widget.hide()

        game = GameWindow(self.parent, sudoku)
        game.show()
