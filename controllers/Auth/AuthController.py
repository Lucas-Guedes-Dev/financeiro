from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.User import User
from db import store

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Usuário e senha são obrigatórios"}), 400

    with store.open_session() as session:
        results = list(session.query(object_type=User).where_equals("username", username).take(1))
        
        if not results:
            return jsonify({"msg": "Credenciais inválidas"}), 401

        user = results[0]

        if not user or not user.check_password(password):
            return jsonify({"msg": "Credenciais inválidas"}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
