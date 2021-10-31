from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class SettingsDialog(QDialog):
    def __init__(self, parent) -> None:
        """
        :param parent: Родитель, MainWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/settings.ui', self)
        self.label.setText("Игра судоку. Создатель: Вязов Глеб, 2021г")
