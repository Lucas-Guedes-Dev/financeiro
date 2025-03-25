from models.BankAccount import BankAccount
from db import store


class BankAccountService:
    def create(self, data: dict):
        """Cria uma nova categoria de despesa a partir de um JSON."""
        bankAccount = BankAccount(**data)
        try:
            with store.open_session() as session:
                session.store(bankAccount)
                session.save_changes()
                return self.get_all(bankAccount.user_id)
        except Exception as e:
            return {"message": str(e)}

    def get_all(self, user_id: str):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            expenses = list(session.query(
                object_type=BankAccount)
                .where_equals('user_id', user_id))

        return [expense.__dict__ for expense in expenses]

    def get_by_id(self, bank_id: str):
        """Recupera uma categoria de despesa pelo ID."""
        with store.open_session() as session:
            bank = session.load(bank_id, object_type=BankAccount)

        if bank is None:
            return {"message": "bank not found"}

        return bank.__dict__

    def get_by_name(self, name: str, user_id: str):
        """Recupera categorias de despesas que correspondem ao nome."""
        with store.open_session() as session:
            banks = list(session.query(
                object_type=BankAccount)
                .where_equals("name", name)
                .where_equals('user_id', user_id))

        return [bank.__dict__ for bank in banks]
