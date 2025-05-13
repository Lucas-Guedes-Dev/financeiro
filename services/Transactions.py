from models.Transactions import Transaction
from db import store

class TransactionService:
    def create(self, data: Transaction, user: str):
        transaction = Transaction(**data, user=user)
        try:
            with store.open_session() as session:
                session.store(transaction)
                session.save_changes()
                return self.get_all()
        except Exception as e:
            return {"message": str(e)}