from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ExpenseCategories import ExpenseCategoriesService

expense_categories_bp = Blueprint('expense_categories', __name__)


@expense_categories_bp.route('/Expense/All', methods=['GET'])
@jwt_required()
def get_all_expense_categories():
    user_id = get_jwt_identity()
    service = ExpenseCategoriesService()
    return service.get_all(user_id), 200


@expense_categories_bp.route('/Expense', methods=['POST'])
@jwt_required()
def create_expense_category():
    data = request.get_json()
    user_id = get_jwt_identity()
    service = ExpenseCategoriesService()
    return jsonify(service.create(data, user_id)), 201
