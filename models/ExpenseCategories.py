import uuid

class ExpenseCategories:
    def __init__(self,id, name: str, description: int, user: str):
        self.id = id
        self.name = name
        self.description = description
        self.user = user