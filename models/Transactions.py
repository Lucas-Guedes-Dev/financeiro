import uuid
from datetime import datetime

class Transaction:
    def __init__(self, user: str, type: str, amount: float, category_id: str, description: str, date: str):
        self.id = str(uuid.uuid1())
        self.user = user
        self.type = type  
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.date = datetime.strptime(date, '%d/%m/%Y').isoformat()