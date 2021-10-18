from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QRadioButton


class Game(QWidget):
    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.sudoku = sudoku
        uic.loadUi('ui/game.ui', self)
        self.current_value = "0"

        self.__setup_ui()

    def __setup_ui(self):
        c = 0
        for i in range(9):
            for j in range(9):
                button = QPushButton(self)
                button.setObjectName(str(i) + str(j))

                if self.sudoku.field[i, j] != 0:
                    button.setText(str(self.sudoku.field[i, j]))
                    c+=1
                else:
                    button.setText("")

                button.clicked.connect(self.__open_item)
                self.ui_field.addWidget(button, i, j)
        print(c)

        x = 30
        y = 500
        for i in range(1, 10):
            radio = QRadioButton(str(i), self)
            radio.setObjectName("radio" + str(i))
            radio.toggled.connect(self.__change_digit)
            radio.setGeometry(x, y, 30, 30)
            x += 50

    def __change_digit(self):
        name = self.sender().objectName()
        print(name)
        self.current_value = name[5:]

    def __open_item(self):
        if self.current_value == "0":
            return
        coords = self.sender().objectName()
        y, x = int(coords[0]), int(coords[1])
        y += 1
        x += 1
        pres_button = self.ui_field.itemAt(9*(y-1) + x - 1).widget()
        print(pres_button.text())
        pres_button.setText(self.current_value)
