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
        self.buttonBox.accepted.connect(WinDialog.__run)

    @staticmethod
    def __run() -> None:
        """Запуск главного окна"""
        from ui.MainWindow import MainWindow
        main = MainWindow()
        main.show()
