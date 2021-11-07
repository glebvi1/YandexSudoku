from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class SaveSudokuDialog(QDialog):
    def __init__(self, parent, sudoku) -> None:
        """
        :param parent: Родитель, MainWindow
        :param sudoku: Текущая судоку
        """
        super().__init__(parent)
        self.sudoku = sudoku
        self.parent = parent
        uic.loadUi('ui/save_sudoku.ui', self)
        self.btn_save.clicked.connect(self.save_sudoku)

    def save_sudoku(self) -> None:
        """Сохраняем судоку в файл"""
        import ui.MainWindow as mw

        name = self.filename.text()
        time = self.parent.time.toString()
        count_hints = self.parent.count_hints
        if name == "":
            return

        if mw.user is not None:
            current_user = self.sudoku.save_game(name, time, count_hints, mw.user)
            mw.user = current_user
        else:
            self.sudoku.save_game(name, time, count_hints, mw.user)
        self.close()
        self.parent.parent.restart()
