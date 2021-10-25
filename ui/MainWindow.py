import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from NewGameWindow import NewGameWindow
from SettingsDialog import SettingsDialog
from UploadSudokuWindow import UploadSudokuWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main_window.ui', self)
        self.buttons = (self.btn_settings, self.btn_new_game, self.btn_upload_game)

        self.__setup_ui()

    def __setup_ui(self):
        for button in self.buttons:
            button.clicked.connect(self.__navigation)

    def __navigation(self):
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
