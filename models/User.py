import uuid
import bcrypt


class User:
    def __init__(self, id, username: str, password: str, person: str = "",
                 admin: bool = False):
        self.id = id
        self.username = username
        self.password = password
        self.person = person
        self.admin = admin

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password.encode())
