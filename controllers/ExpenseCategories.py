# app/controllers/expense_categories_controller.py

from flask import Blueprint, jsonify, request
from services.ExpenseCategories import ExpenseCategoriesService

expense_categories_bp = Blueprint('expense_categories', __name__)

@expense_categories_bp.route('/Expense/All', methods=['GET'])
def get_all_expense_categories():
    service = ExpenseCategoriesService()
    return service.get_all(), 200

@expense_categories_bp.route('/Expense', methods=['POST'])
def create_expense_category():
    data = request.get_json()
    service = ExpenseCategoriesService()
    return jsonify(service.create(data)), 201
