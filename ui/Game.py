from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton

from PyQt5 import uic


class Game(QWidget):
    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.sudoku = sudoku
        uic.loadUi('ui/game.ui', self)

        self.__setup_ui()

    def __setup_ui(self):
        for i in range(9):
            for j in range(9):
                label = QLabel(self)
                label.setObjectName(str(i) + str(j))
                label.setText("0")
                self.ui_field.addWidget(label, i, j)

        x = 30
        y = 500
        for i in range(1, 10):
            radio = QRadioButton(str(i), self)
            radio.setObjectName("radio" + str(i))
            radio.toggled.connect(self.__open_item)
            radio.setGeometry(x, y, 30, 30)
            x += 50

    def __open_item(self):
        pass

