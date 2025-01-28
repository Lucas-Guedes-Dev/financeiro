import uuid
from datetime import datetime

class Transaction:
    def __init__(self, user_id: str, type: str, amount: float, category_id: str, description: str, date: datetime):
        self.id = str(uuid.uuid1())
        self.user_id = user_id
        self.type = type  
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.date = date.isoformat()