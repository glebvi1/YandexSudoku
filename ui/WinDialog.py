from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class WinDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/win.ui', self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.run)

    def run(self):
        from ui.MainWindow import MainWindow
        main = MainWindow()
        main.show()
