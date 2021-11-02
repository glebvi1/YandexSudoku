class User:
    def __init__(self, uid: int, login: str, name: str, password: str) -> None:
        self.uid = uid
        self.login = login
        self.name = name
        self.password = password

    def __str__(self):
        return f"uid = {self.uid}, login = {self.login}, name = {self.name}, password = {self.password}"
