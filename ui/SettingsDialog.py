from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from dao.db_sudokus_handler import get_sudokus_by_sids


class SettingsDialog(QDialog):

    TEXT = "Игра судоку. Создатель: Вязов Глеб, 2021г"

    def __init__(self, parent) -> None:
        """Конструктор SettingsDialog
        :param parent: Родитель, MainWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/settings.ui', self)
        self.label.setText(SettingsDialog.TEXT)
        self.__setup_ui()

    def __setup_ui(self):
        """Установка текста на диалоговое окно"""
        import ui.MainWindow as mw
        if mw.user is None:
            return
        text = ""
        text += f"\nДобрый день, {mw.user.name}!"
        text += f"\nВсего игр: {len(mw.user.sudokus)}"

        sudokus = get_sudokus_by_sids(mw.user.sudokus)
        for _, filename, time, count_hints, is_solved, n, _ in sudokus:
            text += f"\nСудоку {filename}\nСложность: {SettingsDialog.__get_difficulty(n)}" \
                                   f"\nИспользованно подсказок: {count_hints}" \
                                   f"\n{SettingsDialog.__get_is_solved(is_solved)}"

        self.label.setText(text)

    @staticmethod
    def __get_difficulty(n: int) -> str:
        if n == 0:
            return "легкая"
        return "средняя" if n == 1 else "сложная"

    @staticmethod
    def __get_is_solved(is_solved: bool) -> str:
        return "Решена" if is_solved else "Не решена"
