from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.User import User
from db import store

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data, 'olaaa')
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Usuário e senha são obrigatórios"}), 400

    with store.open_session() as session:
        user = session.query(object_type=User).where_equals(
            "username", username).first()

        if not user or not user.check_password(password):
            return jsonify({"msg": "Credenciais inválidas"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"msg": "Você está logado!", "user_id": user_id}), 200
