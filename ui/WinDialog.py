from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class WinDialog(QDialog):
    def __init__(self, parent) -> None:
        """Конструктор WinDialog
        :param parent: родитель, GameWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/win.ui', self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.__run)

    def __run(self) -> None:
        """Запуск главного окна"""
        import ui.MainWindow as mw
        if mw.user is not None:
            self.parent.sudoku.update_sudoku(self.parent.time, self.parent.count_hints, True, mw.user)
        self.parent.close()
        self.close()
        self.parent.parent.restart()
