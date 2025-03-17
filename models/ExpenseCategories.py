import uuid

class ExpenseCategories:
    def __init__(self, name: str, description: int, user: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.user = user