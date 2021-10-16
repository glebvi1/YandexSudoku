from PyQt5.QtWidgets import QWidget

from PyQt5 import uic


class UploadSudoku(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/upload_sudoku.ui', self)

