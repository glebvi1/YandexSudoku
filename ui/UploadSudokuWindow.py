from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from model.Sudoku import Sudoku
from ui.GameWindow import GameWindow


class UploadSudokuWindow(QWidget):

    def __init__(self, parent) -> None:
        """
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/upload_sudoku.ui', self)
        self.btn_search.clicked.connect(self.__create_sudoku_from_file)
        self.widgets = (self.error, self.btn_search, self.filename, self.label)

    def __create_sudoku_from_file(self) -> None:
        """Запуск игрового окна с судокой из файла
        Метод перехватывает FileNotFoundError"""
        filename = self.filename.text()
        if filename == "":
            self.error.setText("Пустое поле!")
            return
        try:
            sudoku = Sudoku.sudoku_from_file(filename)
        except FileNotFoundError:
            self.error.setText("Такого файла нет!")
            return

        for widget in self.widgets:
            widget.hide()
        game = GameWindow(self.parent, sudoku)
        game.show()
