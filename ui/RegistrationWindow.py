from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLineEdit

from dao.db_handler import registration_user


class RegistrationWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/registration.ui', self)
        self.widgets = (self.btn_reg, self.btn_have_account, self.label, self.login, self.name,
                        self.password, self.error)
        self.__setup_ui()

    def __setup_ui(self):
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_reg.clicked.connect(self.__registration)
        self.btn_have_account.clicked.connect(self.__have_account)

    def __registration(self):
        login = self.login.text()
        name = self.name.text()
        password = self.password.text()
        if len(login) == 0 or len(password) == 0 or len(name) == 0:
            self.error.setText("Неккоректный ввод!")
            return
        user = registration_user(login, name, password)
        if user is None:
            self.error.setText("Вы ввели некоректные данные!")
            return
        from ui.MainWindow import MainWindow
        MainWindow.user = user
        MainWindow.restart()
        print(user)

    def __have_account(self):
        for widget in self.widgets:
            widget.hide()

        from ui.LoginWindow import LoginWindow
        login = LoginWindow(self.parent)
        login.show()
