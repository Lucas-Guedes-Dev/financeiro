from flask import Blueprint, js
from services.BankAccount import BankAccountService

bank_account_bp = Blueprint('bank_account', __name__)


@bank_account_bp.route('/Bank/All', methods=['GET'])
def get_all_bank_account():
    service = BankAccountService()
    return service.get_all(), 200


@bank_account_bp.route('/Bank', methods=['POST'])
def get_all_bank_account():
    service = BankAccountService()
    return service.post(), 200
