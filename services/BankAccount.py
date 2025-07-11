from models.BankAccount import BankAccount
from models.Transactions import Transaction
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
        """Recupera todas as contas bancárias do usuário com saldo calculado a partir das transações."""
        with store.open_session() as session:
            # Recupera todas as contas bancárias do usuário
            contas = list(session.query(object_type=BankAccount)
                        .where_equals('user_id', user_id))

            transacoes = list(session.query(object_type=Transaction)
                            .where_equals('user', user_id))

            saldos_por_conta = {}

            for transacao in transacoes:
                conta_id = transacao.bank_account_id
                valor = abs(transacao.amount)

                if conta_id not in saldos_por_conta:
                    saldos_por_conta[conta_id] = 0.0

                if transacao.type.lower() == 'entrada':
                    saldos_por_conta[conta_id] += valor
                elif transacao.type.lower() == 'saida':
                    saldos_por_conta[conta_id] -= valor

            contas_formatadas = []
            for conta in contas:
                conta_dict = conta.__dict__.copy()
                conta_dict['balance'] = saldos_por_conta.get(conta.id, 0.0)
                contas_formatadas.append(conta_dict)

            return contas_formatadas

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
