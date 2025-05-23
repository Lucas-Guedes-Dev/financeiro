import uuid
from datetime import datetime

class FinancialGoal:
    def __init__(self, id, user_id: str, name: str, target_amount: float, saved_amount: float, deadline: datetime):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.target_amount = target_amount
        self.saved_amount = saved_amount
        self.deadline = deadline.isoformat()