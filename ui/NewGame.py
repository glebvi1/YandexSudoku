from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

from model.Sudoku import Sudoku
from Game import Game


class NewGame(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/new_game.ui', self)
        self.buttons = (self.btn_easy, self.btn_middle, self.btn_hard)
        self.widgets = [self.label, self.label_2]
        self.widgets.extend(self.buttons)

        self.__setup_ui()

    def __setup_ui(self):
        for button in self.buttons:
            button.clicked.connect(self.__generate_sudoku)

    def __generate_sudoku(self):
        sudoku = Sudoku()

        for widget in self.widgets:
            widget.hide()

        game = Game(self, sudoku)
        game.show()
