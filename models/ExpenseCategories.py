import uuid

class ExpenseCategories:
    def __init__(self, name: str, description: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description