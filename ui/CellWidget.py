from PyQt5.QtWidgets import QWidget, QPushButton

from ui.WinDialog import WinDialog


class CellWidget(QWidget):
    def __init__(self, parent) -> None:
        """Конструктор CellWidget
        :param parent: Родитель, MainWindow
        """
        super().__init__(parent)
        self.button = QPushButton(self)
        self.button.clicked.connect(self.__draw)
        self.parent = parent
        self.is_drawn_in_pencil = False
        self.color = "black"
        self.background_color = ""
        self.font_size = "15"

    def __draw(self) -> None:
        """Рисуем на gui"""
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
                self.draw_pen(self.parent.current_value)
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

    def __draw_in_sudoku(self, x: int, y: int, value: int) -> None:
        """Изменяем судоку
        :param x: номер столбеца
        :param y: номер строки
        :param value: значение на эту клетку
        """
        self.parent.sudoku.current_field[y][x] = value
        print(self.parent.sudoku.current_field)

    def draw_pen(self, str_value: str) -> None:
        """Рисуем ручкой
        :param str_value: текст на эту кнопку
        """
        print(str_value)
        self.button.setText(str_value)
        self.color = "black"
        self.font_size = "15"
        self.__set_style()
        self.is_drawn_in_pencil = False
        self.parent.do_paint = True

    def __draw_pencil(self, str_value: str) -> None:
        """Рисуем карандашом
        :param str_value: добавляем к текущем значениям на кнопке
        """
        self.is_drawn_in_pencil = True
        text = self.button.text()
        if text == "":
            self.button.setText(str_value)
            self.color = "red"
            self.font_size = "10"
            self.__set_style()
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
        self.color = "red"
        self.font_size = "10"
        self.__set_style()

    def update_button(self) -> None:
        """Обновляем кнопки с карандашом"""
        if self.is_drawn_in_pencil:
            print("update")
            name = self.button.objectName()[3:]
            y, x = int(name[0]), int(name[1])
            print(y, x)
            variants = self.parent.sudoku.generate_cell_value(x, y, is_main_field=False)
            print(variants)
            new_digit = []
            for digit in self.button.text():
                if digit == "\n" or digit == " ":
                    continue
                if int(digit) in variants:
                    new_digit.append(digit)

            new_text = CellWidget.__variants_to_string(tuple(new_digit))

            self.button.setText(new_text)
            self.color = "red"
            self.font_size = "10"
            self.__set_style()

    def draw_all_variants(self, x, y) -> None:
        """Помечаем кнопку всеми вариантами"""
        if self.button.text() != "" and not self.is_drawn_in_pencil:
            return
        self.is_drawn_in_pencil = True

        variants = self.parent.sudoku.generate_cell_value(x, y, is_main_field=False)
        self.button.setText(CellWidget.__variants_to_string(variants))
        self.color = "red"
        self.font_size = "10"
        self.__set_style()

    @staticmethod
    def __variants_to_string(variants: tuple) -> str:
        """
        :param variants: кортеж из int-ов
        """
        result = ""
        index = 0
        for elem in variants:
            if index % 3 == 0 and index != 0:
                result += "\n"
            else:
                result += " "
            result += str(elem)
            index += 1

        return result

    def __set_style(self) -> None:
        """Устанавливаем стиль кнопки"""
        self.button.setStyleSheet("QPushButton {color: " + self.color + "; background-color: "
                           + self.background_color + "; font-size: " + self.font_size + "px;}")
