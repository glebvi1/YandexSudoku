from __future__ import annotations

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from NewGameWindow import NewGameWindow
from SettingsDialog import SettingsDialog
from UploadSudokuWindow import UploadSudokuWindow
from ui.LoginWindow import LoginWindow

user = None


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """Конструктор MainWindow"""
        super().__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.buttons = (self.btn_settings, self.btn_new_game, self.btn_upload_game, self.btn_login)

        self.__setup_ui()

    @classmethod
    def create_new_window(cls):
        return cls()

    def restart(self):
        """Перезагрузка MainWindow"""
        global main_window
        self.hide()
        main_window = self.create_new_window()
        for button in main_window.buttons:
            button.show()
        main_window.show()

    def __setup_ui(self) -> None:
        """Установка слушателей на кнопки"""
        for button in self.buttons:
            button.clicked.connect(self.__navigation)

    def __navigation(self) -> None:
        """Переключения на окона: 'новая игра', 'загрузка игры', 'настройки', 'авторизация'"""
        name = self.sender().objectName()[4:]
        if name == "settings":
            settings = SettingsDialog(self)
            settings.open()
            return

        for button in self.buttons:
            button.hide()
        self.label.hide()

        if name == "new_game":
            new_game = NewGameWindow(self)
            new_game.show()
        elif name == "upload_game":
            upload_sudoku = UploadSudokuWindow(self)
            upload_sudoku.show()
        elif name == "login":
            login = LoginWindow(self)
            login.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
