from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from model.Sudoku import Sudoku
from ui.GameWindow import GameWindow


class UploadSudokuWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/upload_sudoku.ui', self)
        self.__setup_ui()

    def __setup_ui(self):
        self.btn_search.clicked.connect(self.__create_sudoku_from_file)

    def __create_sudoku_from_file(self):
        filename = self.filename.text()
        if filename == "":
            self.error.setText("Пустое поле!")
            return
        try:
            sudoku = Sudoku.sudoku_from_file(filename)
        except FileNotFoundError as error:
            self.error.setText("Такого файла нет!")
            return

        self.error.hide()
        self.btn_search.hide()
        self.filename.hide()
        self.label.hide()
        game = GameWindow(self.parent, sudoku)
        game.show()
