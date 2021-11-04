from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLineEdit

from dao.db_users_handler import login_user


class LoginWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/login.ui', self)
        self.widgets = (self.btn_login, self.btn_create_account, self.label, self.login,
                        self.password, self.error)
        self.__setup_ui()

    def __setup_ui(self):
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_login.clicked.connect(self.__login)
        self.btn_create_account.clicked.connect(self.__create_account)

    def __login(self):
        login = self.login.text()
        password = self.password.text()
        if len(login) == 0 or len(password) == 0:
            self.error.setText("Неккоректный ввод!")
            return
        user = login_user(login, password)
        if user is None:
            self.error.setText("Вы ввели некоректные данные!")
            return
        from ui.MainWindow import MainWindow
        MainWindow.user = user
        MainWindow.restart()
        print(user)

    def __create_account(self):
        for widget in self.widgets:
            widget.hide()

        from ui.RegistrationWindow import RegistrationWindow
        registration = RegistrationWindow(self.parent)
        registration.show()
