import uuid

class User:
    def __init__(self, name: str, age: int):
        self.id = str(uuid.uuid1())
        self.name = name
        self.age = age