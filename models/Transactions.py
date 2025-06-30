import uuid
from datetime import datetime

class Transaction:
    def __init__(self, id:str, user: str, bank_account_id: str, type: str, amount: float, category_id: str, description: str, date: str):
        self.id = id
        self.user = user
        self.type = type  
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.bank_account_id = bank_account_id
        
        if isinstance(date, str):
            try:
                self.date = datetime.strptime(date, '%d/%m/%Y').isoformat()
            except ValueError:
                self.date = date 
        elif isinstance(date, datetime):
            self.date = date.isoformat()
        else:
            self.date = str(date)