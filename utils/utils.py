import inspect
import uuid
import bcrypt


def validate_json(data: dict, cls: classmethod):
    atributos = list(inspect.signature(cls.__init__).parameters.keys())
    if 'self' in atributos:
        del atributos[0]
    return all(key in data for key in list(atributos))


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def create_id():
    return str(uuid.uuid1())
