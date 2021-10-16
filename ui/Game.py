from PyQt5.QtWidgets import QWidget, QLabel

from PyQt5 import uic


class Game(QWidget):
    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.sudoku = sudoku
        uic.loadUi('ui/game.ui', self)
        self.__draw_field()

    def __draw_field(self):
        for i in range(9):
            for j in range(9):
                label = QLabel(self)
                label.setObjectName(str(i) + str(j))
                label.setText("0")
                self.ui_field.addWidget(label, i, j)

