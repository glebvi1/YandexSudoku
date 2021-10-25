from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class SaveSudokuDialog(QDialog):
    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.sudoku = sudoku
        uic.loadUi('ui/save_sudoku.ui', self)
        self.__setup_ui()

    def __setup_ui(self):
        self.btn_save.clicked.connect(self.save_sudoku)

    def save_sudoku(self):
        name = self.filename.text()
        if name != "":
            self.sudoku.save_game(name)
