from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget

from dao.db_sudokus_handler import get_sudokus_by_sids


class SettingsDialog(QDialog):

    TEXT = "Игра судоку. Создатель: Вязов Глеб, 2021г"

    def __init__(self, parent) -> None:
        """Конструктор SettingsDialog
        :param parent: Родитель, MainWindow
        """
        super().__init__(parent)
        uic.loadUi('ui/settings.ui', self)
        label = QLabel()
        label.setText(SettingsDialog.TEXT)
        self.scroll.setWidget(label)
        self.__setup_ui()

    def __setup_ui(self):
        """Установка текста на диалоговое окно"""
        import ui.MainWindow as mw
        if mw.user is None:
            return

        text = f"\nДобрый день, {mw.user.name}!"
        text += f"\nВсего игр: {len(mw.user.sudokus)}"

        label = QLabel(self)
        label.setText(text)

        layout = QVBoxLayout(self)
        layout.addWidget(label)

        widget = QWidget(self)

        sudokus = get_sudokus_by_sids(mw.user.sudokus)

        for _, filename, time, count_hints, is_solved, n, _ in sudokus:
            label = QLabel(self)

            text = f"\nСудоку {filename}\nСложность: {SettingsDialog.__get_difficulty(n)}" \
                                   f"\nИспользованно подсказок: {count_hints}" \
                                   f"\n{SettingsDialog.__get_is_solved(is_solved)}"

            label.setText(text)
            layout.addWidget(label)

        widget.setLayout(layout)
        self.scroll.setWidget(widget)

    @staticmethod
    def __get_difficulty(n: int) -> str:
        if n == 0:
            return "легкая"
        return "средняя" if n == 1 else "сложная"

    @staticmethod
    def __get_is_solved(is_solved: bool) -> str:
        return "Решена" if is_solved else "Не решена"
