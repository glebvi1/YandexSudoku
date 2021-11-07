class User:
    def __init__(self, uid: int, login: str, name: str, password: str, sudokus=None) -> None:
        """Конструктор User-а"""
        if sudokus is None:
            sudokus = []
        self.uid = uid
        self.login = login
        self.name = name
        self.password = password
        self.sudokus = sudokus

    def __str__(self) -> str:
        """Красивый вывод пользователя"""
        return f"uid = {self.uid}, login = {self.login}, name = {self.name}, password = {self.password}"
