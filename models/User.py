import uuid
import bcrypt


class User:
    def __init__(self, username: str, password: str, person: str = "", admin: bool = False):
        self.id = str(uuid.uuid1())
        self.username = username
        self.password = self.hash_password(password)
        self.person = person
        self.admin = admin

    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def check_password(self, password: str) -> bool:
        if not self.password:
            # print("Erro: Senha armazenada está vazia ou None.")
            return False

        return bcrypt.checkpw(password.encode('utf-8'), self.password)
