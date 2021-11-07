from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class SettingsDialog(QDialog):

    TEXT = "Игра судоку. Создатель: Вязов Глеб, 2021г"

    def __init__(self, parent) -> None:
        """
        :param parent: Родитель, MainWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/settings.ui', self)
        self.label.setText("Игра судоку. Создатель: Вязов Глеб, 2021г")
        self.__setup_ui()

    def __setup_ui(self):
        import ui.MainWindow as mw
        if mw.user is None:
            return
        SettingsDialog.TEXT += f"\nДобрый день, {mw.user.name}!"
        SettingsDialog.TEXT += f"\nВсего игр: {len(mw.user.sudokus)}"

        self.label.setText(SettingsDialog.TEXT)
