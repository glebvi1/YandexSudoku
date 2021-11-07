from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLineEdit

from dao.db_users_handler import login_user


class LoginWindow(QWidget):
    def __init__(self, parent) -> None:
        """Конструктор LoginWindow
        :param parent: MainWindow
        """
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('ui/login.ui', self)
        self.widgets = (self.btn_login, self.btn_create_account, self.label, self.login,
                        self.password, self.error)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        """Установка ui"""
        self.password.setEchoMode(QLineEdit.Password)
        self.btn_login.clicked.connect(self.__login)
        self.btn_create_account.clicked.connect(self.__create_account)

    def __login(self) -> None:
        """Авторизация пользователя"""
        login = self.login.text()
        password = self.password.text()
        if len(login) == 0 or len(password) == 0:
            self.error.setText("Неккоректный ввод!")
            return
        current_user = login_user(login, password)
        if current_user is None:
            self.error.setText("Вы ввели некоректные данные!")
            return
        import ui.MainWindow as mw
        mw.user = current_user
        self.parent.restart()
        self.hide()

    def __create_account(self):
        """Переход на RegistrationWindow"""
        for widget in self.widgets:
            widget.hide()

        from ui.RegistrationWindow import RegistrationWindow
        registration = RegistrationWindow(self.parent)
        registration.show()
