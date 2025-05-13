from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.Transactions import TransactionService

transactions_bp = Blueprint('transactions_bp', __name__)


@transactions_bp.route('/Expense', methods=['POST'])
@jwt_required()
def create_expense_category():
    data = request.get_json()
    user_id = get_jwt_identity()
    service = TransactionService()
    return jsonify(service.create(data, user_id)), 201