from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/settings.ui', self)
        self.__setup_ui()

    def __setup_ui(self):
        self.label.setText("Игра судоку. Создатель: Вязов Глеб, 2021г")
