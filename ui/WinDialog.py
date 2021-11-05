from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class WinDialog(QDialog):
    def __init__(self, parent) -> None:
        """
        :param parent: MainWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/win.ui', self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.__run)

    def __run(self) -> None:
        """Запуск главного окна"""
        self.parent.close()
        self.close()
        self.parent.parent.restart()
