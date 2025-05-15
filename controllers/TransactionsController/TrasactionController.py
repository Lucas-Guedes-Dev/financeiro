from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.Transactions import TransactionService

transactions_bp = Blueprint('transactions_bp', __name__)
service = TransactionService()

@transactions_bp.route('/Transaction', methods=['POST'])
@jwt_required()
def create_transactions():
    data = request.get_json()
    user_id = get_jwt_identity()
    return service.create(data, user_id)

@transactions_bp.route('/Transaction/All', methods=['GET'])
@jwt_required()
def get_all_transactions():
    user_id = get_jwt_identity()
    return jsonify(service.get_all(user_id))

@transactions_bp.route('/Transaction/<id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    user_id = get_jwt_identity()
    return jsonify(service.get_by_id(user_id, id))

@transactions_bp.route('/Transaction/<id>', methods=['PUT'])
@jwt_required()
def update_transaction(id):
    data = request.get_json()
    user_id = get_jwt_identity()
    return jsonify(service.update(user_id, id, data))

@transactions_bp.route('/Transaction/<id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    user_id = get_jwt_identity()
    return jsonify(service.delete(user_id, id))