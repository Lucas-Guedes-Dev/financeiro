import uuid


class BankAccount:
    def __init__(self, id: str, user_id: str, bank_name: str, account_number: str, balance: float):
        self.id = id
        self.user_id = user_id
        self.bank_name = bank_name
        self.account_number = account_number
        self.balance = balance
