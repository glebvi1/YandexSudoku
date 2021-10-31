from PyQt5.QtWidgets import QWidget, QPushButton

from ui.WinDialog import WinDialog


class CellWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.button = QPushButton(self)
        self.button.clicked.connect(self.__draw)
        self.parent = parent
        self.is_drawn_in_pencil = False

    def __draw(self):
        if self.parent.current_value == "0":
            return

        coords = self.sender().objectName()[3:]
        y, x = int(coords[0]), int(coords[1])
        value = int(self.parent.current_value)
        print(y, x)

        # Удаление
        if value == 100:
            self.parent.sudoku.current_field[y][x] = 0
            self.button.setText("")
            self.is_drawn_in_pencil = False
            return

        if self.parent.sudoku.is_correct_event(x, y, value):
            print("correct")
            if self.parent.is_pen:
                self.__draw_in_sudoku(x, y, value)
                self.__draw_pen(self.parent.current_value)
                self.parent.do_paint = True
            else:
                self.__draw_pencil(self.parent.current_value)
            self.parent.error_text = ""
        else:
            self.parent.error_text = "Противоречие!"

        if self.parent.sudoku.is_win():
            self.parent.show()
            print("WIN")
            win = WinDialog(self.parent)
            win.show()

    def __draw_in_sudoku(self, x, y, value: int):
        """Изменяем судоку"""
        self.parent.sudoku.current_field[y][x] = value
        print(self.parent.sudoku.current_field)

    def __draw_pen(self, str_value: str):
        """Изменяем gui ручкой"""
        print(str_value)
        self.button.setText(str_value)
        self.button.setStyleSheet('QPushButton {color: black;}')
        self.is_drawn_in_pencil = False

    def __draw_pencil(self, str_value: str):
        """Изменяем gui карандашом"""
        self.is_drawn_in_pencil = True
        text = self.button.text()
        if text == "":
            self.button.setText(str_value)
            self.button.setStyleSheet('QPushButton {color: red; font-size: 10px;}')
            return

        count = 0
        for elem in text:
            if elem == "\n":
                count = 0
            if elem.isdigit():
                count += 1
            if elem == str_value:
                return
        if count == 3:
            text += f"\n{str_value}"
        else:
            text += f" {str_value}"

        self.button.setText(text)
        self.button.setStyleSheet('QPushButton {color: red; font-size: 10px;}')

    def update_button(self):
        if self.is_drawn_in_pencil:
            print("update")
            name = self.button.objectName()[3:]
            y, x = int(name[0]), int(name[1])
            print(y, x)
            variants = self.parent.sudoku.generate_cell_value(x, y, is_main_field=False)
            print(variants)
            new_digit = ""
            new_text = ""
            for digit in self.button.text():
                if digit == "\n" or digit == " ":
                    continue
                if int(digit) in variants:
                    new_digit += digit

            for i, digit in enumerate(new_digit):
                new_text += digit
                if (i + 1) % 3 == 0:
                    new_text += "\n"
                else:
                    new_text += " "

            self.button.setText(new_text)
            self.button.setStyleSheet('QPushButton {color: red; font-size: 10px;}')