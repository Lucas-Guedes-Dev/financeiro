from flask import Blueprint, request
from services.BankAccount import BankAccountService
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.utils import create_id

bank_account_bp = Blueprint('bank_account', __name__)


@bank_account_bp.route('/BankAccount/All', methods=['GET'])
@jwt_required()
def get_all_bank_account():
    user_id = get_jwt_identity()

    service = BankAccountService()
    return service.get_all(user_id), 200


@bank_account_bp.route('/BankAccount', methods=['POST'])
@jwt_required()
def post_account():
    data = request.json
    user_id = get_jwt_identity()

    data['id'] = create_id()
    data['user_id'] = user_id

    service = BankAccountService()
    return service.create(data), 200
